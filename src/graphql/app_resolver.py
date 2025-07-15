from typing import List, Optional
from graphql.pyutils import description
import strawberry

from src.config.init_config import app_service



@strawberry.input
class CreateApp:
    name: str
    description: str
    
@strawberry.type
class AppType:
    id: int
    name: str
    description: str


@strawberry.type
class Mutation:
    @strawberry.mutation
    def createUser(self, input: CreateApp) -> AppType:
        app = app_service.create_app(input.name, input.description)
        if app.id is None:
            raise ValueError("App ID cannot be None")
        return AppType(
            id=app.id,
            name=app.name,
            description=app.description
        )
        
        
   

@strawberry.type
class Query:
    @strawberry.field
    def hello() -> str:
        return "Hello World"

schema = strawberry.Schema(query=Query, mutation=Mutation) 




    

   




    