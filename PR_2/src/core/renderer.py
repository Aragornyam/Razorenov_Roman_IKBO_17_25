import subprocess


def generate_d2_and_svg(graph: dict, output_svg: str) -> None:
    """Формирование синтаксиса D2 и компиляция SVG."""
    d2_text = "direction: right\n\n"
    
    for u, neighbors in graph.items():
        if not neighbors:
            d2_text += f'"{u}"\n'
        for v in neighbors:
            d2_text += f'"{u}" -> "{v}"\n'

    d2_file = "graph.d2"
    with open(d2_file, 'w', encoding='utf-8') as f:
        f.write(d2_text)
    print(f"Текстовое представление D2 сохранено в {d2_file}")

    try:
        subprocess.run(["d2", "--layout=elk", d2_file, output_svg], check=True)
        print(f"SVG граф успешно сохранен в {output_svg}")
    except FileNotFoundError:
        print("ВНИМАНИЕ: Утилита 'd2' не найдена в PATH.")
        print("Сгенерирован только текстовый файл graph.d2.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка компиляции с движком elk: {e}")
        print("Пробуем скомпилировать со стандартным движком dagre...")
        try:
            subprocess.run(["d2", d2_file, output_svg], check=True)
            print(f"SVG граф (dagre) успешно сохранен в {output_svg}")
        except subprocess.CalledProcessError as e_inner:
            print(f"Ошибка компиляции D2: {e_inner}")
