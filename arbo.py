import subprocess
import networkx as nx
import matplotlib.pyplot as plt

MAX_LINES = 15# Nombre de commits par colonne


def get_branches_for_commit(commit):
    try:
        branches = subprocess.check_output(
            ["git", "branch", "--contains", commit],
            text=True, encoding="utf-8"
        ).splitlines()
        return [b.replace("*", "").strip() for b in branches]
    except:
        return []


def get_git_graph():
    log = subprocess.check_output(
        ['git', 'log', '--pretty=format:%H|%P|%ct|%s', '--all'],
        text=True, encoding="utf-8"
    )

    G = nx.DiGraph()
    commits = []

    for line in log.splitlines():
        commit, parents, timestamp, message = line.split("|", 3)
        parents = parents.split() if parents else []
        timestamp = int(timestamp)
        branches = get_branches_for_commit(commit)
        branch = branches[0] if branches else "unknown"

        commits.append((commit, parents, timestamp, message, branch))
        G.add_node(commit, label=message[:35] + "...", branch=branch)

        for p in parents:
            G.add_edge(p, commit)

    commits = sorted(commits, key=lambda x: x[2])

    pos = {}
    branch_tracks = {}

    for idx, (commit, parents, _, _, branch) in enumerate(commits):

        col = idx // MAX_LINES  # colonne x
        row = idx % MAX_LINES  # ligne y

        if branch not in branch_tracks:
            branch_tracks[branch] = len(branch_tracks) * 0.9

        x = col * 5 + branch_tracks[branch]  # Décalage entre colonnes
        y = -row

        pos[commit] = (x, y)

    return G, pos


def draw_graph(G, pos):
    plt.figure(figsize=(20, 10))

    branches = list(set(nx.get_node_attributes(G, "branch").values()))
    colormap = {b: i for i, b in enumerate(branches)}
    colors = [colormap[G.nodes[n]["branch"]] for n in G.nodes]

    nx.draw(
        G, pos,
        node_color=colors,
        cmap=plt.cm.tab20,
        with_labels=False,
        node_size=350,
        arrows=True
    )

    nx.draw_networkx_labels(
        G, pos,
        labels={n: G.nodes[n]["label"] for n in G.nodes},
        font_size=8
    )

    plt.title("Arbre Git paginé – Style Livre (colonnes)")
    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    graph, pos = get_git_graph()
    draw_graph(graph, pos)
