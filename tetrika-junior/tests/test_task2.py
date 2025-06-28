from collections import defaultdict

from task2.solution import extract_animal_data, save_statistics, collect_animal_statistics


def test_extract_animal_data():
    html = """
    <div id="mw-pages">
      <div class="mw-category-group">
        <ul>
          <li>Аист</li>
          <li>Бобр</li>
          <li>Волк</li>
        </ul>
      </div>
    </div>
    """
    result = extract_animal_data(html)
    assert result == ["Аист", "Бобр", "Волк"]


def test_save_statistics(tmp_path):
    data = defaultdict(int, {'А': 2, 'Б': 1})
    file_path = tmp_path / "test_beasts.csv"
    save_statistics(data, filename=str(file_path))
    content = file_path.read_text(encoding="utf-8").splitlines()
    assert content[0] == "Буква,Количество животных"
    assert "А,2" in content
    assert "Б,1" in content

