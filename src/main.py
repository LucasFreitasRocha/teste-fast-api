import uvicorn
import argparse
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from graphql.app_resolver import schema
from config.init_config import init_config



app = FastAPI()

# Initialize database and create tables
init_config()

# Add GraphQL route
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")




if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    args = parser.parse_args()
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=args.reload,
        reload_includes=[
            "src/main.py",
            "src/graphql/*.py",
            "src/config/*.py",
            "src/data/*.py",
            "src/data/repository/*.py",
            "src/data/service/*.py",
            "src/data/domain/*.py",
            "src/data/model/*.py",
            "src/data/schema/*.py",
            "src/data/schema/user/*.py",
        ]
        if args.reload
        else None,
    )