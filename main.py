from models.author import Author
Author.add_author("Julia Quinn")

authors = Author.list_authors()
print(authors)