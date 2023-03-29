def write(dados: dict):
    print("""
<!DOCTYPE html>
<html>
    <head>
        <title>Trabalho</title>
        <meta charset="utf-8">
        <link rel="stylesheet" href="w3.css">
    </head>
    <body>""")
    
    for data in dados:
        print(f"""
        <div class="w3-container w3-teal">
            <h2>{data['title']}</h2>
        </div>
        <div class="w3-container">
            <p>{data['text']}</p>
        </div>
        """)


    print("""
    </body>
    <footer>
        <p>Scripting no Processamento de Linguagem Natural, 2023</p>
    </footer>
</html>""")



print