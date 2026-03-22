"""Search-tree visualisation (text-based and optional Graphviz)."""

# ── Text-based tree printer (Dùng cho Terminal) ──────────────────────────────

def _fmt_board(state):
    """Compact one-line board string, e.g. |1 2 3|4 _ 5|7 8 6|."""
    b = state.board
    def f(v):
        return str(v) if v else "_"
    return f"|{f(b[0])} {f(b[1])} {f(b[2])}|{f(b[3])} {f(b[4])} {f(b[5])}|{f(b[6])} {f(b[7])} {f(b[8])}|"


def visualize_tree(expanded_nodes, n=15):
    """Print the first *n* expanded nodes as an indented tree."""
    nodes = expanded_nodes[:n]
    if not nodes:
        print("(empty tree)")
        return

    id_map = {id(nd): i for i, nd in enumerate(nodes)}
    children = {i: [] for i in range(len(nodes))}

    for nd in nodes:
        nid = id_map[id(nd)]
        if nd.parent is not None and id(nd.parent) in id_map:
            pid = id_map[id(nd.parent)]
            children[pid].append(nid)

    def _print(idx, prefix="", is_last=True):
        nd = nodes[idx]
        connector = "+-- " if is_last else "|-- "
        label = _fmt_board(nd.state)
        cost = f"g={nd.g} h={nd.h} f={nd.f}"
        action = f"[{nd.action}] " if nd.action else ""

        if idx == 0:
            print(f"Root: {label}  {cost}")
        else:
            print(f"{prefix}{connector}{action}{label}  {cost}")

        ext = "    " if is_last else "|   "
        child_prefix = prefix + ext
        kids = children[idx]
        for i, kid in enumerate(kids):
            _print(kid, child_prefix, i == len(kids) - 1)

    roots = [
        i for i, nd in enumerate(nodes)
        if nd.parent is None or id(nd.parent) not in id_map
    ]
    for root_idx in roots:
        _print(root_idx)


# ── Optional Graphviz renderer (Dùng cho Streamlit hoặc xuất ảnh) ────────────

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

    # Trả về đối tượng dot để vẽ thẳng lên giao diện Web
    if return_dot:
        return dot

    # Hoặc lưu ra file ảnh
    dot.render(filename, view=view, cleanup=True)
    return f"{filename}.png"