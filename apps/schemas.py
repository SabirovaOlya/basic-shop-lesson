import graphene
from graphene_django import DjangoObjectType
from apps.models import Category, Product


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = "__all__"


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"


class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        msg = graphene.String()

    category = graphene.Field(CategoryType)

    def mutate(self, info, name):
        category = Category.objects.create(name=name)
        return CreateCategory(category=category)


class UpdateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()

    category = graphene.Field(CategoryType)

    def mutate(self, info, id, name=None):
        try:
            category = Category.objects.get(pk=id)
        except Category.DoesNotExist:
            raise Exception("Category not found")

        if name:
            category.name = name

        category.save()
        return UpdateCategory(category=category)


class DeleteCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            category = Category.objects.get(pk=id)
        except Category.DoesNotExist:
            raise Exception("Category not found")

        category.delete()
        return DeleteCategory(success=True)


class Query(graphene.ObjectType):
    products = graphene.List(ProductType)
    categories = graphene.List(CategoryType)

    def resolve_categories(self, info):
        return Category.objects.all()

    def resolve_products(self, info):
        return Product.objects.all()


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
