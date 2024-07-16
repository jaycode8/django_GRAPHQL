import graphene
from graphene_django import DjangoObjectType
from .models import Books

class BooksType(DjangoObjectType):
    class Meta:
        model = Books
        fields = "__all__"

class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        description = graphene.String()

    newbook = graphene.Field(BooksType)
    def mutate(self, info, title, description):
        book = Books(title=title, description=description)
        book.save()
        return CreateBook(newbook=book)
    
class UpdateBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        description = graphene.String()

    updatedbook = graphene.Field(BooksType)

    def mutate(self, info, id, title=None, description=None):
        try:
            book = Books.objects.get(pk=id)
        except Books.DoesNotExist:
            raise Exception('Book not found')

        if title:
            book.title = title
        if description:
            book.description = description

        book.save()
        return UpdateBook(updatedbook=book)
    
class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        try:
            book = Books.objects.get(pk=id)
        except Books.DoesNotExist:
            raise Exception('Book not found')

        book.delete()
        return DeleteBook(ok=True)

class Query(graphene.ObjectType):
    books = graphene.List(BooksType)
    book = graphene.Field(BooksType, id = graphene.ID(required=True))

    def resolve_books(self, info):
        return Books.objects.all()
    
    def resolve_book(self, info, id):
        return Books.objects.get(pk=id)
    
class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()
    

schema = graphene.Schema(query=Query, mutation=Mutation)