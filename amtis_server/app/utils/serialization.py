import csv
import io
import html

from fastapi.responses import HTMLResponse, Response


def to_csv(stocks: list[dict], fields: list[str]) -> Response:

    buf = io.StringIO()
    writer = csv.writer(buf, quoting=csv.QUOTE_ALL)

    writer.writerow(fields)
    for s in stocks:
        writer.writerow([s[k] for k in fields])

    return Response(content=buf.getvalue(), media_type="text/csv")


def to_html(stocks: list[dict], fields: list[str]) -> HTMLResponse:

    def f_cell(value):
        return f"<td>{html.escape(str(value))}</td>"
    

    table_body_content = []
    for r in stocks:
        table_body_content.append(
                    f"""
                    <tr>
                    {
                    "\n".join(
                        [ f"{f_cell(r[f])}" for f in fields ])
                    }
                    </tr>
                    """
                    )
        

    content = f"""
    <table>
        <thead>
            <tr>
                {"\n".join(f"<th>{f}</th>" for f in fields)}
            </tr>
        </thead>
        <tbody>
            {"\n".join(table_body_content)}
        </tbody>
    </table>
    """

    return HTMLResponse(content=content, status_code=200)