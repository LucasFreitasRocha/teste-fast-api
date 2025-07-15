import uvicorn
import argparse
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from src.graphql.app_resolver import schema
from src.config.init_config import init_config



app = FastAPI()

# Initialize database and create tables
init_config()

# Add GraphQL route
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")




