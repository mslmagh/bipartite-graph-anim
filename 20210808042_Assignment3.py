from manim import *

class BipartiteVsNonBipartiteV5k(Scene):
    def construct(self):
        intro_title = Text("What is a Bipartite Graph?", font_size=42)
        definition = Text(
            "A graph is bipartite if its vertices can be colored\n"
            "using two colors so that no adjacent vertices share the same color.",
            font_size=28
        )
        definition.next_to(intro_title, DOWN, buff=0.5)

        self.play(Write(intro_title))
        self.wait(1)
        self.play(Write(definition))
        self.wait(3)
        self.play(FadeOut(intro_title), FadeOut(definition))

        bip_title = Text("Is this graph bipartite?", font_size=36)
        self.play(Write(bip_title))
        self.play(bip_title.animate.to_edge(UP))

        bip_explain = Text(
            "Let's try coloring the graph using two colors.", font_size=28
        )
        bip_explain.next_to(bip_title, DOWN)
        self.play(Write(bip_explain))
        self.wait(2)

        radius = 2.2
        bip_nodes_pos = {
            f"V{i}": radius * np.array([
                np.cos(i * PI / 3),
                np.sin(i * PI / 3),
                0
            ])
            for i in range(6)
        }

        bip_edges = [
            ("V0", "V1"), ("V0", "V3"), ("V0", "V5"),
            ("V1", "V2"), ("V1", "V4"),
            ("V2", "V3"), ("V2", "V5"),
            ("V3", "V4"),
            ("V4", "V5")
        ]

        bip_dots = {name: Dot(pos, color=WHITE).scale(0.8) for name, pos in bip_nodes_pos.items()}
        bip_labels = {
            name: Text(name, font_size=24).next_to(bip_dots[name], 0.3 * normalize(bip_nodes_pos[name]))
            for name in bip_dots
        }

        bip_lines = {}
        for u, v in bip_edges:
            line = Line(bip_nodes_pos[u], bip_nodes_pos[v], color=GRAY)
            self.add(line)
            bip_lines[(u, v)] = line

        for name in bip_dots:
            self.add(bip_dots[name], bip_labels[name])

        self.wait(1)

        color_text = Text("Trying to color the graph...", font_size=28).to_edge(DOWN)
        self.play(Write(color_text))
        self.wait(1)

        COLOR_1 = RED
        COLOR_2 = BLUE
        node_colors = {}
        queue = ["V0"]
        node_colors["V0"] = COLOR_1
        self.play(bip_dots["V0"].animate.set_color(COLOR_1), run_time=1.0)

        while queue:
            current = queue.pop(0)
            current_color = node_colors[current]
            neighbor_color = COLOR_2 if current_color == COLOR_1 else COLOR_1

            for neighbor in bip_nodes_pos:
                if neighbor == current:
                    continue
                if (current, neighbor) in bip_lines or (neighbor, current) in bip_lines:
                    if neighbor not in node_colors:
                        node_colors[neighbor] = neighbor_color
                        queue.append(neighbor)
                        self.play(bip_dots[neighbor].animate.set_color(neighbor_color), run_time=1.0)
                    elif node_colors[neighbor] == current_color:
                        conflict = Text(
                            f"⚠️ Conflict between {current} and {neighbor}!",
                            font_size=28,
                            color=RED
                        ).to_edge(DOWN)
                        self.play(Transform(color_text, conflict))
                        self.play(bip_lines[(current, neighbor) if (current, neighbor) in bip_lines else (neighbor, current)].animate.set_color(YELLOW), run_time=1.0)
                        self.wait(2)
                        self.play(Transform(color_text, Text("❌ Not bipartite!", font_size=28, color=RED).to_edge(DOWN)))
                        self.wait(3)
                        break
            else:
                continue
            break
        else:
            success_text = Text("✅ No conflicts — the graph is bipartite.", font_size=28, color=GREEN).to_edge(DOWN)
            self.play(Transform(color_text, success_text))
            self.wait(3)

        self.play(*[FadeOut(mob) for mob in self.mobjects])

        non_title = Text("Is this graph bipartite?", font_size=36)
        self.play(Write(non_title))
        self.play(non_title.animate.to_edge(UP))

        non_explain = Text(
            "Trying the same coloring method...", font_size=28
        )
        non_explain.next_to(non_title, DOWN)
        self.play(Write(non_explain))
        self.wait(2)

        radius = 2.5
        base_angles = [i * 2 * PI / 5 for i in range(5)]

        import math
        angle_v0 = base_angles[0]
        angle_v4 = base_angles[4]

        v0 = np.array([radius * math.cos(angle_v0), radius * math.sin(angle_v0), 0])
        v4 = np.array([radius * math.cos(angle_v4), radius * math.sin(angle_v4), 0])

        vec = v4 - v0
        vec_angle = math.atan2(vec[1], vec[0])
        rotate_angle = -vec_angle

        non_nodes_pos = {}
        for i in range(5):
            x = radius * math.cos(base_angles[i])
            y = radius * math.sin(base_angles[i])
            x_rot = x * math.cos(rotate_angle) - y * math.sin(rotate_angle)
            y_rot = x * math.sin(rotate_angle) + y * math.cos(rotate_angle)
            non_nodes_pos[f"V{i}"] = np.array([x_rot, y_rot, 0])

        non_dots = {name: Dot(pos, color=WHITE).scale(0.8) for name, pos in non_nodes_pos.items()}
        non_labels = {}
        for name, pos in non_nodes_pos.items():
            direction = normalize(pos)
            non_labels[name] = Text(name, font_size=24).next_to(non_dots[name], direction * 0.3)

        non_lines = {}
        non_edges = [
            ("V0", "V1"), ("V1", "V2"), ("V2", "V3"), ("V3", "V4"), ("V4", "V0")
        ]
        for u, v in non_edges:
            line = Line(non_nodes_pos[u], non_nodes_pos[v], color=GRAY)
            self.add(line)
            non_lines[(u, v)] = line

        for name in non_dots:
            self.add(non_dots[name], non_labels[name])

        self.wait(1)

        color_text = Text("Trying to color the graph...", font_size=28).to_edge(DOWN)
        self.play(Write(color_text))
        self.wait(1)

        COLOR_1 = RED
        COLOR_2 = BLUE
        node_colors = {}
        queue = ["V0"]
        node_colors["V0"] = COLOR_1
        self.play(non_dots["V0"].animate.set_color(COLOR_1), run_time=1.0)

        while queue:
            current = queue.pop(0)
            current_color = node_colors[current]
            neighbor_color = COLOR_2 if current_color == COLOR_1 else COLOR_1

            for neighbor in non_nodes_pos:
                if neighbor == current:
                    continue
                if (current, neighbor) in non_lines or (neighbor, current) in non_lines:
                    if neighbor not in node_colors:
                        node_colors[neighbor] = neighbor_color
                        queue.append(neighbor)
                        self.play(non_dots[neighbor].animate.set_color(neighbor_color), run_time=1.0)
                    elif node_colors[neighbor] == current_color:
                        conflict = Text(
                            f"⚠️ Conflict between {current} and {neighbor}!",
                            font_size=28,
                            color=YELLOW
                        ).to_edge(DOWN)
                        self.play(Transform(color_text, conflict))
                        self.play(non_lines[(current, neighbor) if (current, neighbor) in non_lines else (neighbor, current)].animate.set_color(YELLOW), run_time=1.0)
                        self.wait(2)
                        self.play(Transform(color_text, Text("❌ Not bipartite! Odd cycle detected.", font_size=28, color=RED).to_edge(DOWN)))
                        self.wait(3)
                        return

        self.play(Transform(color_text, Text("✅ No conflicts — the graph is bipartite.", font_size=28, color=GREEN).to_edge(DOWN)))
        self.wait(3)
