import tkinter as tk
from tkinter import messagebox, Label
import json
import os
import matplotlib.pyplot as plt
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx

class SemanticNetworkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Semantic Network")

        frame = tk.Frame(root)
        frame.pack(expand=True, fill='both')

        self.canvas = tk.Canvas(frame, width=800, height=600)
        self.canvas.grid(row=0, column=0, columnspan=2)

        self.graph = nx.DiGraph()
        self.load_data()

        self.draw_graph()

        buttons_frame = tk.Frame(root)  # Изменено на root
        buttons_frame.pack(side="top")  # Изменено на pack с side="top"

        self.link_description_label = Label(buttons_frame, text="Описание связи:")
        self.link_description_label.grid(row=0, column=0)

        self.link_description = tk.Entry(buttons_frame)
        self.link_description.grid(row=0, column=1)

        self.node_entry1_label = Label(buttons_frame, text="Узел 1:")
        self.node_entry1_label.grid(row=1, column=0)

        self.node_entry1 = tk.Entry(buttons_frame)
        self.node_entry1.grid(row=1, column=1)

        self.node_entry2_label = Label(buttons_frame, text="Узел 2:")
        self.node_entry2_label.grid(row=2, column=0)

        self.node_entry2 = tk.Entry(buttons_frame)
        self.node_entry2.grid(row=2, column=1)

        self.link_options = [
            "(Gen) Генеративная связь",
            "(Des) Дестинативная связь",
            "(Dir) Директивная связь",
            "(Ins) Инструментальная связь",
            "(Cous) Каузальная связь",
            "(Com) Комитативная связь",
            "(Cor) Коррелятивная связь",
            "(Neg) Негативаня связь",
            "(Lim) Лимитативная связь",
            "(Med) Медиативная связь",
            "(Pos) Поссесивная связь",
            "(Pot) Потенсивная связь",
            "(Res) Результативная связь",
            "(Rep) Репродуктивная связь",
            "(Sit) Ситуативная связь",
            "(Trg) Трансгрессивная связь",
            "(Fin) Финитивная связь"
        ]
        self.link_var = tk.StringVar()
        self.link_var.set(self.link_options[0])
        self.link_menu = tk.OptionMenu(buttons_frame, self.link_var, *self.link_options)
        self.link_menu.grid(row=3, column=0, columnspan=2)

        self.add_link_button = tk.Button(buttons_frame, text="Добавить связь", command=self.add_link)
        self.add_link_button.grid(row=4, column=0, columnspan=2)

        self.show_graph_button = tk.Button(buttons_frame, text="Показать график", command=self.show_graph)
        self.show_graph_button.grid(row=5, column=0, columnspan=2)

        self.save_button = tk.Button(buttons_frame, text="Сохранить", command=self.save_data)
        self.save_button.grid(row=6, column=0, columnspan=2)

        self.search_button = tk.Button(buttons_frame, text="Поиск связей", command=self.search_connectivity)
        self.search_button.grid(row=7, column=0, columnspan=2)

        self.delete_node_button = tk.Button(buttons_frame, text="Удалить узел", command=self.delete_node)
        self.delete_node_button.grid(row=8, column=0, columnspan=2)

        self.delete_edge_button = tk.Button(buttons_frame, text="Удалить связь", command=self.delete_edge)
        self.delete_edge_button.grid(row=9, column=0, columnspan=2)

        self.edit_edge_button = tk.Button(buttons_frame, text="Редактировать связь", command=self.edit_edge)
        self.edit_edge_button.grid(row=10, column=0, columnspan=2)

        self.edit_node_button = tk.Button(buttons_frame, text="Редактировать узел", command=self.edit_node)
        self.edit_node_button.grid(row=11, column=0, columnspan=2)

    # Остальные методы остаются без изменений




    def load_data(self):
        if os.path.exists("semantic_network.json"):
            with open("semantic_network.json", "r") as file:
                try:
                    data = json.load(file)
                    self.graph = nx.DiGraph(data)
                except json.JSONDecodeError:
                    self.graph = nx.DiGraph()
                    messagebox.showwarning("Warning", "Invalid JSON data. Creating an empty graph.")
        else:
            self.graph = nx.DiGraph()

    def save_data(self):
        adjacency_dict = dict(self.graph.adjacency())
        with open("semantic_network.json", "w") as file:
            json.dump(adjacency_dict, file)

    def draw_graph(self):
        graph_window = tk.Toplevel(self.root)
        graph_window.title("Semantic Network Graph")
        fig, ax = plt.subplots(figsize=(10, 8))  # Изменяем размер графика для лучшей видимости
        pos = nx.spring_layout(self.graph, k=1, iterations=50)  # Подбираем k для увеличения расстояния между вершинами
        edge_colors = range(len(self.graph.edges))
        nx.draw_networkx_edges(self.graph, pos, ax=ax, edge_color=edge_colors, width=1.0, alpha=0.7, arrowsize=20)
        nx.draw_networkx_nodes(self.graph, pos, ax=ax, node_size=1000, node_color='skyblue')

        nx.draw_networkx_labels(self.graph, pos, ax=ax, labels={node: node for node in self.graph.nodes()},
                                font_size=10, font_color='black', verticalalignment='center',
                                horizontalalignment='center')

        edge_labels_with_description = {(u, v): f"{data['link_type']}\n{data.get('description', '')}" for u, v, data in
                                        self.graph.edges(data=True)}

        for (u, v), label in edge_labels_with_description.items():
            x = (pos[u][0] + pos[v][0]) / 2
            y = (pos[u][1] + pos[v][1]) / 2
            edge_color = edge_colors[list(self.graph.edges).index((u, v))]
            ax.text(x, y, label, fontsize=8, ha='center', va='center', color=plt.cm.viridis(edge_color))

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas, graph_window)
        toolbar.update()
        canvas.get_tk_widget().pack()

    def edit_node(self):
        all_nodes = self.get_all_nodes()

        # Создаем новое окно для выбора узлов
        node_edit_window = tk.Toplevel(self.root)
        node_edit_window.title("Edit Node")

        # Создаем выпадающий список для выбора узла
        node_label = tk.Label(node_edit_window, text="Node:")
        node_label.grid(row=0, column=0)

        node_var = tk.StringVar()
        node_dropdown = tk.OptionMenu(node_edit_window, node_var, *all_nodes)
        node_dropdown.grid(row=0, column=1)

        # Создаем поле для ввода нового имени узла
        new_name_label = tk.Label(node_edit_window, text="New Node Name:")
        new_name_label.grid(row=1, column=0)

        new_name_entry = tk.Entry(node_edit_window)
        new_name_entry.grid(row=1, column=1)

        # Функция редактирования узла
        def edit_node_action():
            old_node_name = node_var.get().strip()
            new_node_name = new_name_entry.get().strip()
            if old_node_name in self.graph.nodes():
                self.graph = nx.relabel_nodes(self.graph, {old_node_name: new_node_name}, copy=False)
                self.save_data()
                self.draw_graph()
                messagebox.showinfo("Success", "Node '{}' edited.".format(old_node_name))
            else:
                messagebox.showerror("Error", "Node '{}' does not exist.".format(old_node_name))

        # Кнопка для редактирования узла
        edit_button = tk.Button(node_edit_window, text="Edit Node", command=edit_node_action)
        edit_button.grid(row=2, columnspan=2)

    def edit_edge(self):
        connected_nodes = self.get_connected_nodes()

        # Создаем новое окно для редактирования связи
        edge_edit_window = tk.Toplevel(self.root)
        edge_edit_window.title("Edit Edge")

        # Создаем выпадающие списки для выбора узлов
        node1_label = tk.Label(edge_edit_window, text="Node 1:")
        node1_label.grid(row=0, column=0)
        node2_label = tk.Label(edge_edit_window, text="Node 2:")
        node2_label.grid(row=1, column=0)

        node1_var = tk.StringVar()
        node1_dropdown = tk.OptionMenu(edge_edit_window, node1_var, *connected_nodes)
        node1_dropdown.grid(row=0, column=1)

        node2_var = tk.StringVar()
        node2_dropdown = tk.OptionMenu(edge_edit_window, node2_var, *connected_nodes)
        node2_dropdown.grid(row=1, column=1)

        # Создаем выпадающий список для выбора типа связи
        new_link_label = tk.Label(edge_edit_window, text="New Link Type:")
        new_link_label.grid(row=2, column=0)

        new_link_var = tk.StringVar()
        new_link_menu = tk.OptionMenu(edge_edit_window, new_link_var, *self.link_options)
        new_link_menu.grid(row=2, column=1)

        # Создаем поле для ввода нового описания связи
        new_description_label = tk.Label(edge_edit_window, text="New Link Description:")
        new_description_label.grid(row=3, column=0)

        new_description_var = tk.StringVar()
        new_description_entry = tk.Entry(edge_edit_window, textvariable=new_description_var)
        new_description_entry.grid(row=3, column=1)

        # Функция редактирования связи
        def edit_edge_action():
            node_name1 = node1_var.get().strip()
            node_name2 = node2_var.get().strip()
            new_link_type = new_link_var.get().strip()
            new_description = new_description_var.get().strip()
            if node_name1 in self.graph.nodes() and node_name2 in self.graph.nodes():
                if self.graph.has_edge(node_name1, node_name2):
                    self.graph[node_name1][node_name2]['link_type'] = new_link_type
                    self.graph[node_name1][node_name2]['description'] = new_description
                    self.save_data()
                    self.draw_graph()
                    messagebox.showinfo("Success", "Edge between {} and {} edited.".format(node_name1, node_name2))
                else:
                    messagebox.showerror("Error", "There is no edge between {} and {}.".format(node_name1, node_name2))
            else:
                messagebox.showerror("Error", "One or both nodes do not exist!")

        # Кнопка для редактирования связи
        edit_button = tk.Button(edge_edit_window, text="Edit Edge", command=edit_edge_action)
        edit_button.grid(row=4, columnspan=2)

    def get_all_nodes(self):
        return list(self.graph.nodes())

    def delete_node(self):
        all_nodes = self.get_all_nodes()

        # Создаем новое окно для выбора узлов
        node_delete_window = tk.Toplevel(self.root)
        node_delete_window.title("Delete Node")

        # Создаем выпадающий список для выбора узла
        node_label = tk.Label(node_delete_window, text="Node:")
        node_label.grid(row=0, column=0)

        node_var = tk.StringVar()
        node_dropdown = tk.OptionMenu(node_delete_window, node_var, *all_nodes)
        node_dropdown.grid(row=0, column=1)

        # Функция удаления узла
        def delete_node_action():
            node_name = node_var.get().strip()
            if node_name in self.graph.nodes():
                self.graph.remove_node(node_name)
                self.save_data()
                self.draw_graph()
                messagebox.showinfo("Success", "Node '{}' deleted.".format(node_name))
            else:
                messagebox.showerror("Error", "Node '{}' does not exist.".format(node_name))

        # Кнопка для удаления узла
        delete_button = tk.Button(node_delete_window, text="Delete Node", command=delete_node_action)
        delete_button.grid(row=1, columnspan=2)

    def get_connected_nodes(self):
        return list(self.graph.nodes())

    def delete_edge(self):
        connected_nodes = self.get_connected_nodes()

        # Создаем новое окно для выбора узлов
        edge_delete_window = tk.Toplevel(self.root)
        edge_delete_window.title("Delete Edge")

        # Создаем выпадающие списки для выбора узлов
        node1_label = tk.Label(edge_delete_window, text="Node 1:")
        node1_label.grid(row=0, column=0)
        node2_label = tk.Label(edge_delete_window, text="Node 2:")
        node2_label.grid(row=1, column=0)

        node1_var = tk.StringVar()
        node1_dropdown = tk.OptionMenu(edge_delete_window, node1_var, *connected_nodes)
        node1_dropdown.grid(row=0, column=1)

        node2_var = tk.StringVar()
        node2_dropdown = tk.OptionMenu(edge_delete_window, node2_var, *connected_nodes)
        node2_dropdown.grid(row=1, column=1)

        # Функция удаления связи
        def delete_edge_action():
            node_name1 = node1_var.get().strip()
            node_name2 = node2_var.get().strip()
            if node_name1 in self.graph.nodes() and node_name2 in self.graph.nodes():
                if self.graph.has_edge(node_name1, node_name2):
                    self.graph.remove_edge(node_name1, node_name2)
                    self.save_data()
                    self.draw_graph()
                    messagebox.showinfo("Success", "Edge between {} and {} deleted.".format(node_name1, node_name2))
                else:
                    messagebox.showerror("Error", "There is no edge between {} and {}.".format(node_name1, node_name2))
            else:
                messagebox.showerror("Error", "One or both nodes do not exist!")

        # Кнопка для удаления связи
        delete_button = tk.Button(edge_delete_window, text="Delete Edge", command=delete_edge_action)
        delete_button.grid(row=2, columnspan=2)

    def add_link(self):
        node_name1 = self.node_entry1.get().strip()
        node_name2 = self.node_entry2.get().strip()
        link_type = self.link_var.get().strip()
        description = self.link_description.get().strip()  # Получаем введенное описание связи

        if node_name1 and node_name2:
            self.graph.add_edge(node_name1, node_name2, link_type=link_type,
                                description=description)  # Добавляем описание связи
            self.save_data()
            self.draw_graph()
        else:
            messagebox.showerror("Error", "Node names cannot be empty!")

    def show_graph(self):
        self.draw_graph()

    def search_connectivity(self):
        node_name1 = self.node_entry1.get().strip()
        node_name2 = self.node_entry2.get().strip()

        # Check if both nodes exist in the graph
        if node_name1 not in self.graph.nodes() or node_name2 not in self.graph.nodes():
            messagebox.showerror("Error", "One or both nodes do not exist!")
            return

        # Attempt to find all paths between the nodes, considering both directed and undirected edges
        directed_paths = list(nx.all_simple_paths(self.graph, source=node_name1, target=node_name2))
        undirected_graph = self.graph.to_undirected()
        undirected_paths = list(nx.all_simple_paths(undirected_graph, source=node_name1, target=node_name2))

        # Format the paths for display
        directed_paths_str = "\n".join([" -> ".join(path) for path in directed_paths])
        undirected_paths_str = "\n".join([" -> ".join(path) for path in undirected_paths])

        # Display the paths to the user
        if directed_paths:
            messagebox.showinfo("Connectivity (Directed)",
                                f"There exist directed paths between {node_name1} and {node_name2}:\n{directed_paths_str}")
        else:
            messagebox.showinfo("Connectivity (Directed)",
                                f"There are no directed paths between {node_name1} and {node_name2}.")

        if undirected_paths:
            messagebox.showinfo("Connectivity (Undirected)",
                                f"There exist undirected paths between {node_name1} and {node_name2}:\n{undirected_paths_str}")
        else:
            messagebox.showinfo("Connectivity (Undirected)",
                                f"There are no undirected paths between {node_name1} and {node_name2}.")


root = tk.Tk()
app = SemanticNetworkApp(root)
root.mainloop()
