#programas.append({'titulo': titulo, 'link': link, 'inicial': inicial, 'final': final, 'imagem': imagem, 'detalhes': detalhes})

class Program:
    def __init__(self, title, link, start, end, img, details):
        self.title = title
        self.link = link
        self.start = start
        self.end = end
        self.img = img
        self.details = details
        