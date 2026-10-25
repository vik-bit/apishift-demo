# apishift-demo

A small sales-report package written for **pandas 1.x**. It uses APIs that pandas 2.0 removed
(`DataFrame.append`, `iteritems`, `mad`, `read_csv(squeeze=)`, `to_csv(line_terminator=)`), so its
tests fail on pandas 2.2.

It exists to show [APIShift](https://github.com/vik-bit/apishift) at work: APIShift scanned this
repository, fixed the removed APIs (exact codemods for the mechanical ones, an LLM for the rest),
verified every change with the test suite below, and opened a pull request.

```bash
pip install -r requirements.txt
python -m pytest
```
