import sys
sys.path.append('.')
from src.retail_insights.data_layer import DataLayer


def test_load_sample():
    dl = DataLayer()
    df = dl.load_csv('sample_data/sample_sales.csv')
    assert df is not None
    assert len(df) >= 1


def test_summarizer_and_qa_smoke():
    dl = DataLayer()
    dl.load_csv('sample_data/sample_sales.csv')
    from src.retail_insights.summarizer import Summarizer
    from src.retail_insights.qa_engine import QAEngine

    s = Summarizer(dl)
    text = s.summarize('Give me a short summary of sales')
    assert isinstance(text, str)

    q = QAEngine(dl)
    a = q.ask('Which product line underperformed in Q4?')
    assert isinstance(a, str)
