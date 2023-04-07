#programas.append({'titulo': titulo, 'link': link, 'inicial': inicial, 'final': final, 'imagem': imagem, 'detalhes': detalhes})

class Program:
    def __init__(self, title, link, start, end, img, days, details):
        self.title = title
        self.link = link
        self.start = start
        self.end = end
        self.img = img
        self.day = days
        self.details = details

    def isComplete(self):
        return self.title and self.link and self.start and self.end and self.img

        