# visualization.py
def render_tree_graphviz(expanded_nodes, n=15, filename="search_tree", view=False, return_dot=False):
    """Render the first *n* expanded nodes via Graphviz."""
    try:
        from graphviz import Digraph
    except ImportError:
        print("[visualization] graphviz not installed — skipping render.")
        return None

    nodes = expanded_nodes[:n]
    if not nodes:
        return None

    id_map = {id(nd): str(i) for i, nd in enumerate(nodes)}
    dot = Digraph(format="png")
    dot.attr("node", shape="box", fontname="Consolas", fontsize="10")

    for nd in nodes:
        nid = id_map[id(nd)]
        b = nd.state.board
        def f(v):
            return str(v) if v else "_"
        label = (
            f"{f(b[0])} {f(b[1])} {f(b[2])}\n"
            f"{f(b[3])} {f(b[4])} {f(b[5])}\n"
            f"{f(b[6])} {f(b[7])} {f(b[8])}\n"
            f"g={nd.g} h={nd.h} f={nd.f}"
        )
        dot.node(nid, label)
        if nd.parent is not None and id(nd.parent) in id_map:
            dot.edge(id_map[id(nd.parent)], nid, label=nd.action or "")

    if return_dot:
        return dot

    dot.render(filename, view=view, cleanup=True)
    return f"{filename}.png"