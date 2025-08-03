# from pathlib import Path

# from invoke import task


# @task
# def generate(c, model, fields):
#     filename = Path(f"src/models/{model}.py")

#     filename.parent.mkdir(parents=True, exist_ok=True)

#     class_name = model.capitalize()

#     parsed_fields = []

#     imports = {"str", "int", "float", "bool"}

#     for field in fields.split(","):
#         name_type = field.strip().split(":")

#         if len(name_type) != 2:
#             raise ValueError(f"Campo inválido: '{field}'. Use formato nome:tipo")

#         name, type_ = name_type

#         parsed_fields.append(f"    {name.strip()}: {type_.strip()}")

#         imports.add(type_.strip())

#     import_line = "from sqlmodel import SQLModel, Field"

#     if any(t not in {"str", "int", "float", "bool"} for t in imports):
#         import_line += "\nfrom typing import " + ", ".join(
#             sorted(imports - {"str", "int", "float", "bool"})
#         )

#     content = f"""{import_line}
# class {class_name}(SQLModel, table=True):
# {chr(10).join(parsed_fields)}
# """

#     filename.write_text(content)

#     print(f"✅ Modelo gerado: {filename}")


# from invoke import task
# from pathlib import Path

# @task
# def generate(c, model, fields):
#     # Normalizações
#     class_name = model.capitalize()
#     model_file = Path(f"src/models/{model}.py")
#     route_file = Path(f"src/routes/{model}.py")
#     model_file.parent.mkdir(parents=True, exist_ok=True)
#     route_file.parent.mkdir(parents=True, exist_ok=True)

#     # Preparar os campos e tipos
#     parsed_fields = []
#     imports = {"str", "int", "float", "bool"}
#     for field in fields.split(","):
#         name_type = field.strip().split(":")
#         if len(name_type) != 2:
#             raise ValueError(f"Campo inválido: '{field}'. Use nome:tipo")
#         name, type_ = name_type
#         parsed_fields.append(f"    {name.strip()}: {type_.strip()}")
#         imports.add(type_.strip())

#     # Geração da model
#     import_line = "from sqlmodel import SQLModel, Field"
#     if any(t not in {"str", "int", "float", "bool"} for t in imports):
#         import_line += "\nfrom typing import " + ", ".join(sorted(imports - {"str", "int", "float", "bool"}))

#     model_content = f"""{import_line}

# class {class_name}(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
# {chr(10).join(parsed_fields)}
# """

#     model_file.write_text(model_content)
#     print(f"✅ Modelo gerado: {model_file}")

#     # Geração das rotas
#     route_content = f"""from fastapi import APIRouter, HTTPException
# from sqlmodel import Session, select

# from src.config.database import engine
# from src.models.{model} import {class_name}

# router = APIRouter(prefix="/{model}", tags=["{class_name}"])

# @router.get("/")
# def get_all():
#     with Session(engine) as session:
#         return session.exec(select({class_name})).all()

# @router.get("/{{id}}")
# def get_by_id(id: int):
#     with Session(engine) as session:
#         result = session.get({class_name}, id)
#         if not result:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         return result

# @router.post("/")
# def create(data: {class_name}):
#     with Session(engine) as session:
#         session.add(data)
#         session.commit()
#         session.refresh(data)
#         return data

# @router.put("/{{id}}")
# def update(id: int, data: {class_name}):
#     with Session(engine) as session:
#         db_item = session.get({class_name}, id)
#         if not db_item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         for key, value in data.dict().items():
#             setattr(db_item, key, value)
#         session.commit()
#         session.refresh(db_item)
#         return db_item

# @router.patch("/{{id}}")
# def partial_update(id: int, data: dict):
#     with Session(engine) as session:
#         db_item = session.get({class_name}, id)
#         if not db_item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         for key, value in data.items():
#             setattr(db_item, key, value)
#         session.commit()
#         session.refresh(db_item)
#         return db_item

# @router.delete("/{{id}}")
# def delete(id: int):
#     with Session(engine) as session:
#         item = session.get({class_name}, id)
#         if not item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         session.delete(item)
#         session.commit()
#         return {{ "success": True }}
# """

#     route_file.write_text(route_content)
#     print(f"✅ Rotas geradas: {route_file}")


# from invoke import task
# from pathlib import Path

# @task
# def generate(c, model, fields):
#     class_name = model.capitalize()

#     # Paths
#     model_file = Path(f"src/models/{model}.py")
#     controller_file = Path(f"src/controllers/{model}.py")
#     route_file = Path(f"src/routes/{model}.py")

#     # Criar diretórios se não existirem
#     model_file.parent.mkdir(parents=True, exist_ok=True)
#     controller_file.parent.mkdir(parents=True, exist_ok=True)
#     route_file.parent.mkdir(parents=True, exist_ok=True)

#     # Parse dos campos e tipos
#     parsed_fields = []
#     imports = {"str", "int", "float", "bool"}
#     for field in fields.split(","):
#         parts = field.strip().split(":")
#         if len(parts) != 2:
#             raise ValueError(f"Campo inválido: '{field}'. Use nome:tipo")
#         name, type_ = parts
#         parsed_fields.append(f"    {name.strip()}: {type_.strip()}")
#         imports.add(type_.strip())

#     # Geração model.py
#     import_line = "from sqlmodel import SQLModel, Field"
#     if any(t not in {"str", "int", "float", "bool"} for t in imports):
#         extras = sorted(imports - {"str", "int", "float", "bool"})
#         import_line += "\nfrom typing import " + ", ".join(extras)

#     model_content = f"""{import_line}

# class {class_name}(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
# {chr(10).join(parsed_fields)}
# """
#     model_file.write_text(model_content)
#     print(f"✅ Modelo gerado: {model_file}")

#     # Geração controller.py
#     controller_content = f"""from sqlmodel import Session, select
# from fastapi import HTTPException
# from src.config.database import engine
# from src.models.{model} import {class_name}

# def get_all():
#     with Session(engine) as session:
#         return session.exec(select({class_name})).all()

# def get_by_id(id: int):
#     with Session(engine) as session:
#         item = session.get({class_name}, id)
#         if not item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         return item

# def create(data: {class_name}):
#     with Session(engine) as session:
#         session.add(data)
#         session.commit()
#         session.refresh(data)
#         return data

# def update(id: int, data: {class_name}):
#     with Session(engine) as session:
#         db_item = session.get({class_name}, id)
#         if not db_item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         for key, value in data.dict().items():
#             setattr(db_item, key, value)
#         session.commit()
#         session.refresh(db_item)
#         return db_item

# def partial_update(id: int, data: dict):
#     with Session(engine) as session:
#         db_item = session.get({class_name}, id)
#         if not db_item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         for key, value in data.items():
#             setattr(db_item, key, value)
#         session.commit()
#         session.refresh(db_item)
#         return db_item

# def delete(id: int):
#     with Session(engine) as session:
#         item = session.get({class_name}, id)
#         if not item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         session.delete(item)
#         session.commit()
#         return {{ "success": True }}
# """
#     controller_file.write_text(controller_content)
#     print(f"✅ Controller gerado: {controller_file}")

#     # Geração routes.py
#     route_content = f"""from fastapi import APIRouter
# from src.controllers.{model} import (
#     get_all,
#     get_by_id,
#     create,
#     update,
#     partial_update,
#     delete,
# )
# from src.models.{model} import {class_name}

# router = APIRouter(prefix="/{model}", tags=["{class_name}"])

# @router.get("/")
# def route_get_all():
#     return get_all()

# @router.get("/{{id}}")
# def route_get_by_id(id: int):
#     return get_by_id(id)

# @router.post("/")
# def route_create(data: {class_name}):
#     return create(data)

# @router.put("/{{id}}")
# def route_update(id: int, data: {class_name}):
#     return update(id, data)

# @router.patch("/{{id}}")
# def route_partial_update(id: int, data: dict):
#     return partial_update(id, data)

# @router.delete("/{{id}}")
# def route_delete(id: int):
#     return delete(id)
# """
#     route_file.write_text(route_content)
#     print(f"✅ Routes geradas: {route_file}")


# from pathlib import Path

# from invoke import task


# @task
# def generate(c, model, fields):
#     class_name = model.capitalize()

#     # Paths
#     model_file = Path(f"src/models/{model}.py")
#     controller_file = Path(f"src/controllers/{model}.py")
#     route_file = Path(f"src/routes/{model}.py")

#     # Criar diretórios
#     model_file.parent.mkdir(parents=True, exist_ok=True)
#     controller_file.parent.mkdir(parents=True, exist_ok=True)
#     route_file.parent.mkdir(parents=True, exist_ok=True)

#     # Parse dos campos e tipos
#     parsed_fields = []
#     imports = {"str", "int", "float", "bool"}
#     for field in fields.split(","):
#         parts = field.strip().split(":")
#         if len(parts) != 2:
#             raise ValueError(f"Campo inválido: '{field}'. Use nome:tipo")
#         name, type_ = parts
#         parsed_fields.append(f"    {name.strip()}: {type_.strip()}")
#         imports.add(type_.strip())

#     # Geração model.py
#     import_line = "from sqlmodel import SQLModel, Field"
#     if any(t not in {"str", "int", "float", "bool"} for t in imports):
#         extras = sorted(imports - {"str", "int", "float", "bool"})
#         import_line += "\nfrom typing import " + ", ".join(extras)

#     model_content = f"""{import_line}

# class {class_name}(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
# {chr(10).join(parsed_fields)}
# """
#     model_file.write_text(model_content)
#     print(f"✅ Modelo gerado: {model_file}")

#     # Geração controller.py
#     controller_content = f"""from sqlmodel import Session, select
# from fastapi import HTTPException
# from src.config.database import engine
# from src.models.{model} import {class_name}

# def get_all():
#     with Session(engine) as session:
#         return session.exec(select({class_name})).all()

# def get_by_id(id: int):
#     with Session(engine) as session:
#         item = session.get({class_name}, id)
#         if not item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         return item

# def create(data: {class_name}):
#     with Session(engine) as session:
#         session.add(data)
#         session.commit()
#         session.refresh(data)
#         return data

# def update(id: int, data: {class_name}):
#     with Session(engine) as session:
#         db_item = session.get({class_name}, id)
#         if not db_item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         for key, value in data.dict().items():
#             setattr(db_item, key, value)
#         session.commit()
#         session.refresh(db_item)
#         return db_item

# def partial_update(id: int, data: dict):
#     with Session(engine) as session:
#         db_item = session.get({class_name}, id)
#         if not db_item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         for key, value in data.items():
#             setattr(db_item, key, value)
#         session.commit()
#         session.refresh(db_item)
#         return db_item

# def delete(id: int):
#     with Session(engine) as session:
#         item = session.get({class_name}, id)
#         if not item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         session.delete(item)
#         session.commit()
#         return {{ "success": True }}
# """
#     controller_file.write_text(controller_content)
#     print(f"✅ Controller gerado: {controller_file}")

#     # Geração routes.py com dependência JWT
#     route_content = f"""from fastapi import APIRouter, Depends
# from src.controllers.{model} import (
#     get_all,
#     get_by_id,
#     create,
#     update,
#     partial_update,
#     delete,
# )
# from src.models.{model} import {class_name}
# from src.auth import verify_jwt_token

# router = APIRouter(
#     prefix="/{model}",
#     tags=["{class_name}"],
#     dependencies=[Depends(verify_jwt_token)]
# )

# @router.get("/")
# def route_get_all():
#     return get_all()

# @router.get("/{{id}}")
# def route_get_by_id(id: int):
#     return get_by_id(id)

# @router.post("/")
# def route_create(data: {class_name}):
#     return create(data)

# @router.put("/{{id}}")
# def route_update(id: int, data: {class_name}):
#     return update(id, data)

# @router.patch("/{{id}}")
# def route_partial_update(id: int, data: dict):
#     return partial_update(id, data)

# @router.delete("/{{id}}")
# def route_delete(id: int):
#     return delete(id)
# """
#     route_file.write_text(route_content)
#     print(f"✅ Routes geradas: {route_file}")


# from invoke import task
# from pathlib import Path

# @task
# def generate(c, model, fields):
#     class_name = model.capitalize()

#     # Paths
#     model_file = Path(f"src/models/{model}.py")
#     controller_file = Path(f"src/controllers/{model}.py")
#     route_file = Path(f"src/routes/{model}.py")

#     # Criar diretórios
#     model_file.parent.mkdir(parents=True, exist_ok=True)
#     controller_file.parent.mkdir(parents=True, exist_ok=True)
#     route_file.parent.mkdir(parents=True, exist_ok=True)

#     # Parse dos campos e tipos
#     parsed_fields = []
#     imports = {"str", "int", "float", "bool"}
#     for field in fields.split(","):
#         parts = field.strip().split(":")
#         if len(parts) != 2:
#             raise ValueError(f"Campo inválido: '{field}'. Use nome:tipo")
#         name, type_ = parts
#         parsed_fields.append(f"    {name.strip()}: {type_.strip()}")
#         imports.add(type_.strip())

#     # Geração model.py
#     import_line = "from sqlmodel import SQLModel, Field"
#     if any(t not in {"str", "int", "float", "bool"} for t in imports):
#         extras = sorted(imports - {"str", "int", "float", "bool"})
#         import_line += "\nfrom typing import " + ", ".join(extras)

#     model_content = f"""{import_line}

# class {class_name}(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
# {chr(10).join(parsed_fields)}
# """
#     model_file.write_text(model_content)
#     print(f"✅ Modelo gerado: {model_file}")

#     # Geração controller.py
#     controller_content = f"""from sqlmodel import Session, select
# from fastapi import HTTPException
# from src.config.database import engine
# from src.models.{model} import {class_name}

# def get_all():
#     with Session(engine) as session:
#         return session.exec(select({class_name})).all()

# def get_by_id(id: int):
#     with Session(engine) as session:
#         item = session.get({class_name}, id)
#         if not item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         return item

# def create(data: {class_name}):
#     with Session(engine) as session:
#         session.add(data)
#         session.commit()
#         session.refresh(data)
#         return data

# def update(id: int, data: {class_name}):
#     with Session(engine) as session:
#         db_item = session.get({class_name}, id)
#         if not db_item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         for key, value in data.dict().items():
#             setattr(db_item, key, value)
#         session.commit()
#         session.refresh(db_item)
#         return db_item

# def partial_update(id: int, data: dict):
#     with Session(engine) as session:
#         db_item = session.get({class_name}, id)
#         if not db_item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         for key, value in data.items():
#             setattr(db_item, key, value)
#         session.commit()
#         session.refresh(db_item)
#         return db_item

# def delete(id: int):
#     with Session(engine) as session:
#         item = session.get({class_name}, id)
#         if not item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         session.delete(item)
#         session.commit()
#         return {{ "success": True }}
# """
#     controller_file.write_text(controller_content)
#     print(f"✅ Controller gerado: {controller_file}")

#     # Geração routes.py com dependência JWT
#     route_content = f"""from fastapi import APIRouter, Depends
# from src.controllers.{model} import (
#     get_all,
#     get_by_id,
#     create,
#     update,
#     partial_update,
#     delete,
# )
# from src.models.{model} import {class_name}
# from src.security.verify_jwt_token import verify_jwt_token

# router = APIRouter(
#     prefix="/{model}",
#     tags=["{class_name}"],
#     dependencies=[Depends(verify_jwt_token)]
# )

# @router.get("/")
# def route_get_all():
#     return get_all()

# @router.get("/{{id}}")
# def route_get_by_id(id: int):
#     return get_by_id(id)

# @router.post("/")
# def route_create(data: {class_name}):
#     return create(data)

# @router.put("/{{id}}")
# def route_update(id: int, data: {class_name}):
#     return update(id, data)

# @router.patch("/{{id}}")
# def route_partial_update(id: int, data: dict):
#     return partial_update(id, data)

# @router.delete("/{{id}}")
# def route_delete(id: int):
#     return delete(id)
# """
#     route_file.write_text(route_content)
#     print(f"✅ Routes geradas: {route_file}")


# from pathlib import Path

# from invoke import task


# @task
# def generate(c, model, fields):
#     class_name = model.capitalize()
#     model_file = Path(f"src/models/{model}.py")
#     controller_file = Path(f"src/controllers/{model}.py")
#     route_file = Path(f"src/routes/{model}.py")

#     # Criar diretórios
#     model_file.parent.mkdir(parents=True, exist_ok=True)
#     controller_file.parent.mkdir(parents=True, exist_ok=True)
#     route_file.parent.mkdir(parents=True, exist_ok=True)

#     # Parse dos campos
#     parsed_fields = []
#     imports = {"str", "int", "float", "bool"}
#     for field in fields.split(","):
#         parts = field.strip().split(":")
#         if len(parts) != 2:
#             raise ValueError(f"Campo inválido: '{field}'. Use nome:tipo")
#         name, type_ = parts
#         parsed_fields.append(f"    {name.strip()}: {type_.strip()}")
#         imports.add(type_.strip())

#     # model.py
#     import_line = "from sqlmodel import SQLModel, Field"
#     typing_imports = sorted(imports - {"str", "int", "float", "bool"})
#     if typing_imports:
#         import_line += f"\nfrom typing import {', '.join(typing_imports)}"

#     model_content = f"""{import_line}

# class {class_name}(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
# {chr(10).join(parsed_fields)}
# """
#     model_file.write_text(model_content)
#     print(f"✅ Modelo gerado: {model_file}")

#     # controller.py
#     controller_content = f"""from sqlmodel import Session, select
# from fastapi import HTTPException
# from src.config.database import engine
# from src.models.{model} import {class_name}

# def get_all():
#     with Session(engine) as session:
#         return session.exec(select({class_name})).all()

# def get_by_id(id: int):
#     with Session(engine) as session:
#         item = session.get({class_name}, id)
#         if not item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         return item

# def create(data: {class_name}):
#     with Session(engine) as session:
#         session.add(data)
#         session.commit()
#         session.refresh(data)
#         return data

# def update(id: int, data: {class_name}):
#     with Session(engine) as session:
#         db_item = session.get({class_name}, id)
#         if not db_item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         for key, value in data.dict().items():
#             setattr(db_item, key, value)
#         session.commit()
#         session.refresh(db_item)
#         return db_item

# def partial_update(id: int, data: dict):
#     with Session(engine) as session:
#         db_item = session.get({class_name}, id)
#         if not db_item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         for key, value in data.items():
#             setattr(db_item, key, value)
#         session.commit()
#         session.refresh(db_item)
#         return db_item

# def delete(id: int):
#     with Session(engine) as session:
#         item = session.get({class_name}, id)
#         if not item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         session.delete(item)
#         session.commit()
#         return {{ "success": True }}
# """
#     controller_file.write_text(controller_content)
#     print(f"✅ Controller gerado: {controller_file}")

#     # routes.py com auth
#     route_content = f"""from fastapi import APIRouter, Depends
# from src.controllers.{model} import (
#     get_all,
#     get_by_id,
#     create,
#     update,
#     partial_update,
#     delete,
# )
# from src.models.{model} import {class_name}
# from src.security.verify_jwt_token import verify_jwt_token

# {model}_routes = APIRouter(
#     prefix="/{model}",
#     tags=["{class_name}"],
#     dependencies=[Depends(verify_jwt_token)]
# )

# @{model}_routes.get("/")
# def route_get_all():
#     return get_all()

# @{model}_routes.get("/{{id}}")
# def route_get_by_id(id: int):
#     return get_by_id(id)

# @{model}_routes.post("/")
# def route_create(data: {class_name}):
#     return create(data)

# @{model}_routes.put("/{{id}}")
# def route_update(id: int, data: {class_name}):
#     return update(id, data)

# @{model}_routes.patch("/{{id}}")
# def route_partial_update(id: int, data: dict):
#     return partial_update(id, data)

# @{model}_routes.delete("/{{id}}")
# def route_delete(id: int):
#     return delete(id)
# """
#     route_file.write_text(route_content)
#     print(f"✅ Rotas geradas: {route_file}")

#     # Atualiza src/private_routes.py
#     private_routes_file = Path("src/private_routes.py")

#     if private_routes_file.exists():
#         existing = private_routes_file.read_text()

#         import_line = f"from src.routes.{model} import {model}_routes"
#         append_line = f"{model}_routes"

#         if import_line not in existing:
#             existing = import_line + "\n" + existing

#         if "private_routes = [" in existing and append_line not in existing:
#             existing = existing.replace(
#                 "private_routes = [", f"private_routes = [{append_line}, "
#             )

#         private_routes_file.write_text(existing)
#         print(f"✅ private_routes.py atualizado com {model}_routes")
#     else:
#         print("⚠️  src/private_routes.py não encontrado.")


# from invoke import task
# from pathlib import Path
# import re


# @task
# def generate(c, model, fields):
#     class_name = model.capitalize()
#     model_file = Path(f"src/models/{model}.py")
#     controller_file = Path(f"src/controllers/{model}.py")
#     route_file = Path(f"src/routes/{model}.py")

#     # Criar diretórios
#     model_file.parent.mkdir(parents=True, exist_ok=True)
#     controller_file.parent.mkdir(parents=True, exist_ok=True)
#     route_file.parent.mkdir(parents=True, exist_ok=True)

#     # Parse dos campos
#     parsed_fields = []
#     imports = {"str", "int", "float", "bool"}
#     for field in fields.split(","):
#         parts = field.strip().split(":")
#         if len(parts) != 2:
#             raise ValueError(f"Campo inválido: '{field}'. Use nome:tipo")
#         name, type_ = parts
#         parsed_fields.append(f"    {name.strip()}: {type_.strip()}")
#         imports.add(type_.strip())

#     # model.py
#     import_line = "from sqlmodel import SQLModel, Field"
#     typing_imports = sorted(imports - {"str", "int", "float", "bool"})
#     if typing_imports:
#         import_line += f"\nfrom typing import {', '.join(typing_imports)}"

#     model_content = f"""{import_line}

# class {class_name}(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
# {chr(10).join(parsed_fields)}
# """
#     model_file.write_text(model_content)
#     print(f"✅ Modelo gerado: {model_file}")

#     # controller.py
#     controller_content = f"""from sqlmodel import Session, select
# from fastapi import HTTPException
# from src.config.database import engine
# from src.models.{model} import {class_name}

# def get_all():
#     with Session(engine) as session:
#         return session.exec(select({class_name})).all()

# def get_by_id(id: int):
#     with Session(engine) as session:
#         item = session.get({class_name}, id)
#         if not item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         return item

# def create(data: {class_name}):
#     with Session(engine) as session:
#         session.add(data)
#         session.commit()
#         session.refresh(data)
#         return data

# def update(id: int, data: {class_name}):
#     with Session(engine) as session:
#         db_item = session.get({class_name}, id)
#         if not db_item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         for key, value in data.dict().items():
#             setattr(db_item, key, value)
#         session.commit()
#         session.refresh(db_item)
#         return db_item

# def partial_update(id: int, data: dict):
#     with Session(engine) as session:
#         db_item = session.get({class_name}, id)
#         if not db_item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         for key, value in data.items():
#             setattr(db_item, key, value)
#         session.commit()
#         session.refresh(db_item)
#         return db_item

# def delete(id: int):
#     with Session(engine) as session:
#         item = session.get({class_name}, id)
#         if not item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         session.delete(item)
#         session.commit()
#         return {{ "success": True }}
# """
#     controller_file.write_text(controller_content)
#     print(f"✅ Controller gerado: {controller_file}")

#     # route.py com JWT
#     route_content = f"""from fastapi import APIRouter, Depends
# from src.controllers.{model} import (
#     get_all,
#     get_by_id,
#     create,
#     update,
#     partial_update,
#     delete,
# )
# from src.models.{model} import {class_name}
# from src.security.verify_jwt_token import verify_jwt_token

# {model}_routes = APIRouter(
#     prefix="/{model}",
#     tags=["{class_name}"],
#     dependencies=[Depends(verify_jwt_token)]
# )

# @{model}_routes.get("/")
# def route_get_all():
#     return get_all()

# @{model}_routes.get("/{{id}}")
# def route_get_by_id(id: int):
#     return get_by_id(id)

# @{model}_routes.post("/")
# def route_create(data: {class_name}):
#     return create(data)

# @{model}_routes.put("/{{id}}")
# def route_update(id: int, data: {class_name}):
#     return update(id, data)

# @{model}_routes.patch("/{{id}}")
# def route_partial_update(id: int, data: dict):
#     return partial_update(id, data)

# @{model}_routes.delete("/{{id}}")
# def route_delete(id: int):
#     return delete(id)
# """
#     route_file.write_text(route_content)
#     print(f"✅ Rotas geradas: {route_file}")

#     # Atualizar private_routes.py corretamente
#     private_routes_file = Path("src/private_routes.py")

#     if private_routes_file.exists():
#         existing = private_routes_file.read_text()

#         import_line = f"from src.routes.{model} import {model}_routes"
#         route_entry = f"{model}_routes"

#         # Adiciona import se não existir
#         if import_line not in existing:
#             existing = import_line + "\n" + existing

#         # Regex para localizar o array de private_routes
#         pattern = r"(private_routes\s*=\s*\[)(.*?)(\])"
#         match = re.search(pattern, existing, flags=re.DOTALL)

#         if match:
#             start, middle, end = match.groups()
#             routes = [r.strip() for r in middle.split(",") if r.strip()]
#             if route_entry not in routes:
#                 routes.append(route_entry)
#             updated_middle = ", ".join(routes)
#             new_routes_block = f"{start}{updated_middle}{end}"
#             existing = re.sub(pattern, new_routes_block, existing, flags=re.DOTALL)

#             private_routes_file.write_text(existing)
#             print(f"✅ private_routes.py atualizado com {model}_routes")
#         else:
#             print("⚠️  Não foi possível localizar private_routes = [...]")
#     else:
#         print("⚠️  src/private_routes.py não encontrado.")


# import re
# from pathlib import Path

# from invoke import task


# @task
# def generate(c, model, fields):
#     class_name = model.capitalize()
#     model_file = Path(f"src/models/{model}.py")
#     controller_file = Path(f"src/controllers/{model}.py")
#     route_file = Path(f"src/routes/{model}.py")

#     # Criar diretórios
#     model_file.parent.mkdir(parents=True, exist_ok=True)
#     controller_file.parent.mkdir(parents=True, exist_ok=True)
#     route_file.parent.mkdir(parents=True, exist_ok=True)

#     # Parse dos campos
#     parsed_fields = []
#     imports = {"str", "int", "float", "bool"}
#     for field in fields.split(","):
#         parts = field.strip().split(":")
#         if len(parts) != 2:
#             raise ValueError(f"Campo inválido: '{field}'. Use nome:tipo")
#         name, type_ = parts
#         parsed_fields.append(f"    {name.strip()}: {type_.strip()}")
#         imports.add(type_.strip())

#     # model.py
#     import_line = "from sqlmodel import SQLModel, Field"
#     typing_imports = sorted(imports - {"str", "int", "float", "bool"})
#     if typing_imports:
#         import_line += f"\nfrom typing import {', '.join(typing_imports)}"

#     model_content = f"""{import_line}

# class {class_name}(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
# {chr(10).join(parsed_fields)}
# """
#     model_file.write_text(model_content)
#     print(f"✅ Modelo gerado: {model_file}")

#     # controller.py
#     controller_content = f"""from sqlmodel import Session, select
# from fastapi import HTTPException
# from src.config.database import engine
# from src.models.{model} import {class_name}

# def get_all():
#     with Session(engine) as session:
#         return session.exec(select({class_name})).all()

# def get_by_id(id: int):
#     with Session(engine) as session:
#         item = session.get({class_name}, id)
#         if not item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         return item

# def create(data: {class_name}):
#     with Session(engine) as session:
#         session.add(data)
#         session.commit()
#         session.refresh(data)
#         return data

# def update(id: int, data: {class_name}):
#     with Session(engine) as session:
#         db_item = session.get({class_name}, id)
#         if not db_item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         for key, value in data.dict().items():
#             setattr(db_item, key, value)
#         session.commit()
#         session.refresh(db_item)
#         return db_item

# def partial_update(id: int, data: dict):
#     with Session(engine) as session:
#         db_item = session.get({class_name}, id)
#         if not db_item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         for key, value in data.items():
#             setattr(db_item, key, value)
#         session.commit()
#         session.refresh(db_item)
#         return db_item

# def delete(id: int):
#     with Session(engine) as session:
#         item = session.get({class_name}, id)
#         if not item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         session.delete(item)
#         session.commit()
#         return {{ "success": True }}
# """
#     controller_file.write_text(controller_content)
#     print(f"✅ Controller gerado: {controller_file}")

#     # route.py (sem prefix/tags)
#     route_content = f"""from fastapi import APIRouter, Depends
# from src.controllers.{model} import (
#     get_all,
#     get_by_id,
#     create,
#     update,
#     partial_update,
#     delete,
# )
# from src.models.{model} import {class_name}
# from src.security.verify_jwt_token import verify_jwt_token

# {model}_routes = APIRouter(
#     dependencies=[Depends(verify_jwt_token)]
# )

# @{model}_routes.get("/")
# def route_get_all():
#     return get_all()

# @{model}_routes.get("/{{id}}")
# def route_get_by_id(id: int):
#     return get_by_id(id)

# @{model}_routes.post("/")
# def route_create(data: {class_name}):
#     return create(data)

# @{model}_routes.put("/{{id}}")
# def route_update(id: int, data: {class_name}):
#     return update(id, data)

# @{model}_routes.patch("/{{id}}")
# def route_partial_update(id: int, data: dict):
#     return partial_update(id, data)

# @{model}_routes.delete("/{{id}}")
# def route_delete(id: int):
#     return delete(id)
# """
#     route_file.write_text(route_content)
#     print(f"✅ Rotas geradas: {route_file}")

#     # Atualizar private_routes.py corretamente
#     private_routes_file = Path("src/private_routes.py")

#     if private_routes_file.exists():
#         existing = private_routes_file.read_text()

#         import_line = f"from src.routes.{model} import {model}_routes"
#         route_entry = f"{model}_routes"

#         # Adiciona import se não existir
#         if import_line not in existing:
#             existing = import_line + "\n" + existing

#         # Regex para localizar o array de private_routes
#         pattern = r"(private_routes\s*=\s*\[)(.*?)(\])"
#         match = re.search(pattern, existing, flags=re.DOTALL)

#         if match:
#             start, middle, end = match.groups()
#             routes = [r.strip() for r in middle.split(",") if r.strip()]
#             if route_entry not in routes:
#                 routes.append(route_entry)
#             updated_middle = ", ".join(routes)
#             new_routes_block = f"{start}{updated_middle}{end}"
#             existing = re.sub(pattern, new_routes_block, existing, flags=re.DOTALL)

#             private_routes_file.write_text(existing)
#             print(f"✅ private_routes.py atualizado com {model}_routes")
#         else:
#             print("⚠️  Não foi possível localizar private_routes = [...]")
#     else:
#         print("⚠️  src/private_routes.py não encontrado.")


# from invoke import task
# from pathlib import Path
# import re


# @task
# def generate(c, model, fields):
#     class_name = model.capitalize()
#     model_file = Path(f"src/models/{model}.py")
#     controller_file = Path(f"src/controllers/{model}.py")
#     route_file = Path(f"src/routes/{model}.py")

#     # Criar diretórios
#     model_file.parent.mkdir(parents=True, exist_ok=True)
#     controller_file.parent.mkdir(parents=True, exist_ok=True)
#     route_file.parent.mkdir(parents=True, exist_ok=True)

#     # Parse dos campos
#     parsed_fields = []
#     imports = {"str", "int", "float", "bool"}
#     for field in fields.split(","):
#         parts = field.strip().split(":")
#         if len(parts) != 2:
#             raise ValueError(f"Campo inválido: '{field}'. Use nome:tipo")
#         name, type_ = parts
#         parsed_fields.append(f"    {name.strip()}: {type_.strip()}")
#         imports.add(type_.strip())

#     # model.py
#     import_line = "from sqlmodel import SQLModel, Field"
#     typing_imports = sorted(imports - {"str", "int", "float", "bool"})
#     if typing_imports:
#         import_line += f"\nfrom typing import {', '.join(typing_imports)}"

#     model_content = f"""{import_line}

# class {class_name}(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
# {chr(10).join(parsed_fields)}
# """
#     model_file.write_text(model_content)
#     print(f"✅ Modelo gerado: {model_file}")

#     # controller.py
#     controller_content = f"""from sqlmodel import Session, select
# from fastapi import HTTPException
# from src.config.database import engine
# from src.models.{model} import {class_name}

# def get_all():
#     with Session(engine) as session:
#         return session.exec(select({class_name})).all()

# def get_by_id(id: int):
#     with Session(engine) as session:
#         item = session.get({class_name}, id)
#         if not item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         return item

# def create(data: {class_name}):
#     with Session(engine) as session:
#         session.add(data)
#         session.commit()
#         session.refresh(data)
#         return data

# def update(id: int, data: {class_name}):
#     with Session(engine) as session:
#         db_item = session.get({class_name}, id)
#         if not db_item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         for key, value in data.dict().items():
#             setattr(db_item, key, value)
#         session.commit()
#         session.refresh(db_item)
#         return db_item

# def partial_update(id: int, data: dict):
#     with Session(engine) as session:
#         db_item = session.get({class_name}, id)
#         if not db_item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         for key, value in data.items():
#             setattr(db_item, key, value)
#         session.commit()
#         session.refresh(db_item)
#         return db_item

# def delete(id: int):
#     with Session(engine) as session:
#         item = session.get({class_name}, id)
#         if not item:
#             raise HTTPException(status_code=404, detail="{class_name} not found")
#         session.delete(item)
#         session.commit()
#         return {{ "success": True }}
# """
#     controller_file.write_text(controller_content)
#     print(f"✅ Controller gerado: {controller_file}")

#     # routes.py com rotas explícitas, sem prefix nem tags
#     route_content = f"""from fastapi import APIRouter, Depends
# from src.controllers.{model} import (
#     get_all,
#     get_by_id,
#     create,
#     update,
#     partial_update,
#     delete,
# )
# from src.models.{model} import {class_name}
# from src.security.verify_jwt_token import verify_jwt_token

# {model}_routes = APIRouter(
#     dependencies=[Depends(verify_jwt_token)]
# )

# @{model}_routes.get("/{model}")
# def route_get_all():
#     return get_all()

# @{model}_routes.get("/{model}/{{id}}")
# def route_get_by_id(id: int):
#     return get_by_id(id)

# @{model}_routes.post("/{model}")
# def route_create(data: {class_name}):
#     return create(data)

# @{model}_routes.put("/{model}/{{id}}")
# def route_update(id: int, data: {class_name}):
#     return update(id, data)

# @{model}_routes.patch("/{model}/{{id}}")
# def route_partial_update(id: int, data: dict):
#     return partial_update(id, data)

# @{model}_routes.delete("/{model}/{{id}}")
# def route_delete(id: int):
#     return delete(id)
# """
#     route_file.write_text(route_content)
#     print(f"✅ Rotas geradas: {route_file}")

#     # Atualizar src/private_routes.py
#     private_routes_file = Path("src/private_routes.py")

#     if private_routes_file.exists():
#         existing = private_routes_file.read_text()

#         import_line = f"from src.routes.{model} import {model}_routes"
#         route_entry = f"{model}_routes"

#         if import_line not in existing:
#             existing = import_line + "\n" + existing

#         pattern = r"(private_routes\s*=\s*\[)(.*?)(\])"
#         match = re.search(pattern, existing, flags=re.DOTALL)

#         if match:
#             start, middle, end = match.groups()
#             routes = [r.strip() for r in middle.split(",") if r.strip()]
#             if route_entry not in routes:
#                 routes.append(route_entry)
#             updated_middle = ", ".join(routes)
#             new_routes_block = f"{start}{updated_middle}{end}"
#             existing = re.sub(pattern, new_routes_block, existing, flags=re.DOTALL)

#             private_routes_file.write_text(existing)
#             print(f"✅ private_routes.py atualizado com {model}_routes")
#         else:
#             print("⚠️  Não foi possível localizar private_routes = [...]")
#     else:
#         print("⚠️  src/private_routes.py não encontrado.")


# import re
# from pathlib import Path

# from invoke import task

# GENERIC_REPO_PATH = Path("src/repositories/generic_repository.py")

# GENERIC_REPO_CONTENT = """from sqlmodel import Session, select
# from src.config.database import engine
# from fastapi import HTTPException

# def get_all(model_class):
#     with Session(engine) as session:
#         return session.exec(select(model_class)).all()

# def get_by_id(model_class, id: int):
#     with Session(engine) as session:
#         item = session.get(model_class, id)
#         if not item:
#             raise HTTPException(status_code=404, detail=f"{model_class.__name__} not found")
#         return item

# def create(model_instance):
#     with Session(engine) as session:
#         session.add(model_instance)
#         session.commit()
#         session.refresh(model_instance)
#         return model_instance

# def update(model_class, id: int, new_data):
#     with Session(engine) as session:
#         db_item = session.get(model_class, id)
#         if not db_item:
#             raise HTTPException(status_code=404, detail=f"{model_class.__name__} not found")
#         for key, value in new_data.dict().items():
#             setattr(db_item, key, value)
#         session.commit()
#         session.refresh(db_item)
#         return db_item

# def partial_update(model_class, id: int, data: dict):
#     with Session(engine) as session:
#         db_item = session.get(model_class, id)
#         if not db_item:
#             raise HTTPException(status_code=404, detail=f"{model_class.__name__} not found")
#         for key, value in data.items():
#             setattr(db_item, key, value)
#         session.commit()
#         session.refresh(db_item)
#         return db_item

# def delete(model_class, id: int):
#     with Session(engine) as session:
#         item = session.get(model_class, id)
#         if not item:
#             raise HTTPException(status_code=404, detail=f"{model_class.__name__} not found")
#         session.delete(item)
#         session.commit()
#         return {{"success": True}}
# """


# @task
# def generate(c, model, fields):
#     class_name = model.capitalize()
#     model_file = Path(f"src/models/{model}.py")
#     controller_file = Path(f"src/controllers/{model}.py")
#     route_file = Path(f"src/routes/{model}.py")

#     # Criar diretórios
#     model_file.parent.mkdir(parents=True, exist_ok=True)
#     controller_file.parent.mkdir(parents=True, exist_ok=True)
#     route_file.parent.mkdir(parents=True, exist_ok=True)
#     GENERIC_REPO_PATH.parent.mkdir(parents=True, exist_ok=True)

#     # Criar generic_repository.py se não existir
#     if not GENERIC_REPO_PATH.exists():
#         GENERIC_REPO_PATH.write_text(GENERIC_REPO_CONTENT)
#         print(f"✅ generic_repository.py criado em {GENERIC_REPO_PATH}")

#     # Parse dos campos
#     parsed_fields = []
#     imports = {"str", "int", "float", "bool"}
#     for field in fields.split(","):
#         parts = field.strip().split(":")
#         if len(parts) != 2:
#             raise ValueError(f"Campo inválido: '{field}'. Use nome:tipo")
#         name, type_ = parts
#         parsed_fields.append(f"    {name.strip()}: {type_.strip()}")
#         imports.add(type_.strip())

#     # model.py
#     import_line = "from sqlmodel import SQLModel, Field"
#     typing_imports = sorted(imports - {"str", "int", "float", "bool"})
#     if typing_imports:
#         import_line += f"\nfrom typing import {', '.join(typing_imports)}"

#     model_content = f"""{import_line}

# class {class_name}(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
# {chr(10).join(parsed_fields)}
# """
#     model_file.write_text(model_content)
#     print(f"✅ Modelo gerado: {model_file}")

#     # controller.py chamando repositório genérico
#     controller_content = f"""from fastapi import HTTPException
# from src.models.{model} import {class_name}
# from src.repositories.generic_repository import (
#     get_all,
#     get_by_id,
#     create,
#     update,
#     partial_update,
#     delete,
# )

# def get_all_controller():
#     return get_all({class_name})

# def get_by_id_controller(id: int):
#     return get_by_id({class_name}, id)

# def create_controller(data: {class_name}):
#     return create(data)

# def update_controller(id: int, data: {class_name}):
#     return update({class_name}, id, data)

# def partial_update_controller(id: int, data: dict):
#     return partial_update({class_name}, id, data)

# def delete_controller(id: int):
#     return delete({class_name}, id)
# """
#     controller_file.write_text(controller_content)
#     print(f"✅ Controller gerado: {controller_file}")

#     # routes.py com rotas explícitas, sem prefix nem tags
#     route_content = f"""from fastapi import APIRouter, Depends
# from src.controllers.{model} import (
#     get_all_controller,
#     get_by_id_controller,
#     create_controller,
#     update_controller,
#     partial_update_controller,
#     delete_controller,
# )
# from src.models.{model} import {class_name}
# from src.security.verify_jwt_token import verify_jwt_token

# {model}_routes = APIRouter(
#     dependencies=[Depends(verify_jwt_token)]
# )

# @{model}_routes.get("/{model}")
# def route_get_all():
#     return get_all_controller()

# @{model}_routes.get("/{model}/{{id}}")
# def route_get_by_id(id: int):
#     return get_by_id_controller(id)

# @{model}_routes.post("/{model}")
# def route_create(data: {class_name}):
#     return create_controller(data)

# @{model}_routes.put("/{model}/{{id}}")
# def route_update(id: int, data: {class_name}):
#     return update_controller(id, data)

# @{model}_routes.patch("/{model}/{{id}}")
# def route_partial_update(id: int, data: dict):
#     return partial_update_controller(id, data)

# @{model}_routes.delete("/{model}/{{id}}")
# def route_delete(id: int):
#     return delete_controller(id)
# """
#     route_file.write_text(route_content)
#     print(f"✅ Rotas geradas: {route_file}")

#     # Atualizar src/private_routes.py
#     private_routes_file = Path("src/private_routes.py")

#     if private_routes_file.exists():
#         existing = private_routes_file.read_text()

#         import_line = f"from src.routes.{model} import {model}_routes"
#         route_entry = f"{model}_routes"

#         if import_line not in existing:
#             existing = import_line + "\n" + existing

#         pattern = r"(private_routes\s*=\s*\[)(.*?)(\])"
#         match = re.search(pattern, existing, flags=re.DOTALL)

#         if match:
#             start, middle, end = match.groups()
#             routes = [r.strip() for r in middle.split(",") if r.strip()]
#             if route_entry not in routes:
#                 routes.append(route_entry)
#             updated_middle = ", ".join(routes)
#             new_routes_block = f"{start}{updated_middle}{end}"
#             existing = re.sub(pattern, new_routes_block, existing, flags=re.DOTALL)

#             private_routes_file.write_text(existing)
#             print(f"✅ private_routes.py atualizado com {model}_routes")
#         else:
#             print("⚠️  Não foi possível localizar private_routes = [...]")
#     else:
#         print("⚠️  src/private_routes.py não encontrado.")


# import re
# import subprocess
# from pathlib import Path

# from invoke import task

# GENERIC_REPO_PATH = Path("src/repositories/generic_repository.py")

# GENERIC_REPO_CONTENT = """from sqlmodel import Session, select
# from src.config.database import engine
# from fastapi import HTTPException

# def get_all(model_class):
#     with Session(engine) as session:
#         return session.exec(select(model_class)).all()

# def get_by_id(model_class, id: int):
#     with Session(engine) as session:
#         item = session.get(model_class, id)
#         if not item:
#             raise HTTPException(status_code=404, detail=f"{model_class.__name__} not found")
#         return item

# def create(model_instance):
#     with Session(engine) as session:
#         session.add(model_instance)
#         session.commit()
#         session.refresh(model_instance)
#         return model_instance

# def update(model_class, id: int, new_data):
#     with Session(engine) as session:
#         db_item = session.get(model_class, id)
#         if not db_item:
#             raise HTTPException(status_code=404, detail=f"{model_class.__name__} not found")
#         for key, value in new_data.dict().items():
#             setattr(db_item, key, value)
#         session.commit()
#         session.refresh(db_item)
#         return db_item

# def partial_update(model_class, id: int, data: dict):
#     with Session(engine) as session:
#         db_item = session.get(model_class, id)
#         if not db_item:
#             raise HTTPException(status_code=404, detail=f"{model_class.__name__} not found")
#         for key, value in data.items():
#             setattr(db_item, key, value)
#         session.commit()
#         session.refresh(db_item)
#         return db_item

# def delete(model_class, id: int):
#     with Session(engine) as session:
#         item = session.get(model_class, id)
#         if not item:
#             raise HTTPException(status_code=404, detail=f"{model_class.__name__} not found")
#         session.delete(item)
#         session.commit()
#         return {{"success": True}}
# """


# @task
# def generate(c, model, fields):
#     class_name = model.capitalize()
#     model_file = Path(f"src/models/{model}.py")
#     controller_file = Path(f"src/controllers/{model}.py")
#     route_file = Path(f"src/routes/{model}.py")

#     # Criar diretórios
#     model_file.parent.mkdir(parents=True, exist_ok=True)
#     controller_file.parent.mkdir(parents=True, exist_ok=True)
#     route_file.parent.mkdir(parents=True, exist_ok=True)
#     GENERIC_REPO_PATH.parent.mkdir(parents=True, exist_ok=True)

#     # Criar generic_repository.py se não existir
#     if not GENERIC_REPO_PATH.exists():
#         GENERIC_REPO_PATH.write_text(GENERIC_REPO_CONTENT)
#         print(f"✅ generic_repository.py criado em {GENERIC_REPO_PATH}")

#     # Parse dos campos
#     parsed_fields = []
#     imports = {"str", "int", "float", "bool"}
#     for field in fields.split(","):
#         parts = field.strip().split(":")
#         if len(parts) != 2:
#             raise ValueError(f"Campo inválido: '{field}'. Use nome:tipo")
#         name, type_ = parts
#         parsed_fields.append(f"    {name.strip()}: {type_.strip()}")
#         imports.add(type_.strip())

#     # model.py
#     import_line = "from sqlmodel import SQLModel, Field"
#     typing_imports = sorted(imports - {"str", "int", "float", "bool"})
#     if typing_imports:
#         import_line += f"\nfrom typing import {', '.join(typing_imports)}"

#     model_content = f"""{import_line}

# class {class_name}(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
# {chr(10).join(parsed_fields)}
# """
#     model_file.write_text(model_content)
#     print(f"✅ Modelo gerado: {model_file}")

#     # controller.py chamando repositório genérico
#     controller_content = f"""from fastapi import HTTPException
# from src.models.{model} import {class_name}
# from src.repositories.generic_repository import (
#     get_all,
#     get_by_id,
#     create,
#     update,
#     partial_update,
#     delete,
# )

# def get_all_controller():
#     return get_all({class_name})

# def get_by_id_controller(id: int):
#     return get_by_id({class_name}, id)

# def create_controller(data: {class_name}):
#     return create(data)

# def update_controller(id: int, data: {class_name}):
#     return update({class_name}, id, data)

# def partial_update_controller(id: int, data: dict):
#     return partial_update({class_name}, id, data)

# def delete_controller(id: int):
#     return delete({class_name}, id)
# """
#     controller_file.write_text(controller_content)
#     print(f"✅ Controller gerado: {controller_file}")

#     # routes.py com rotas explícitas, sem prefix nem tags
#     route_content = f"""from fastapi import APIRouter, Depends
# from src.controllers.{model} import (
#     get_all_controller,
#     get_by_id_controller,
#     create_controller,
#     update_controller,
#     partial_update_controller,
#     delete_controller,
# )
# from src.models.{model} import {class_name}
# from src.security.verify_jwt_token import verify_jwt_token

# {model}_routes = APIRouter(
#     dependencies=[Depends(verify_jwt_token)]
# )

# @{model}_routes.get("/{model}")
# def route_get_all():
#     return get_all_controller()

# @{model}_routes.get("/{model}/{{id}}")
# def route_get_by_id(id: int):
#     return get_by_id_controller(id)

# @{model}_routes.post("/{model}")
# def route_create(data: {class_name}):
#     return create_controller(data)

# @{model}_routes.put("/{model}/{{id}}")
# def route_update(id: int, data: {class_name}):
#     return update_controller(id, data)

# @{model}_routes.patch("/{model}/{{id}}")
# def route_partial_update(id: int, data: dict):
#     return partial_update_controller(id, data)

# @{model}_routes.delete("/{model}/{{id}}")
# def route_delete(id: int):
#     return delete_controller(id)
# """
#     route_file.write_text(route_content)
#     print(f"✅ Rotas geradas: {route_file}")

#     # Atualizar src/private_routes.py
#     private_routes_file = Path("src/private_routes.py")

#     if private_routes_file.exists():
#         existing = private_routes_file.read_text()

#         import_line = f"from src.routes.{model} import {model}_routes"
#         route_entry = f"{model}_routes"

#         if import_line not in existing:
#             existing = import_line + "\n" + existing

#         pattern = r"(private_routes\s*=\s*\[)(.*?)(\])"
#         match = re.search(pattern, existing, flags=re.DOTALL)

#         if match:
#             start, middle, end = match.groups()
#             routes = [r.strip() for r in middle.split(",") if r.strip()]
#             if route_entry not in routes:
#                 routes.append(route_entry)
#             updated_middle = ", ".join(routes)
#             new_routes_block = f"{start}{updated_middle}{end}"
#             existing = re.sub(pattern, new_routes_block, existing, flags=re.DOTALL)

#             private_routes_file.write_text(existing)
#             print(f"✅ private_routes.py atualizado com {model}_routes")
#         else:
#             print("⚠️  Não foi possível localizar private_routes = [...]")
#     else:
#         print("⚠️  src/private_routes.py não encontrado.")

#     # Formatar com ruff na pasta src
#     try:
#         subprocess.run(["ruff", "src", "--fix"], check=True)
#         print("✅ Código formatado com ruff")
#     except Exception as e:
#         print(f"⚠️ Erro ao formatar código com ruff: {e}")


import re
import subprocess
from pathlib import Path

from invoke import task

GENERIC_REPO_PATH = Path("src/repositories/generic_repository.py")

GENERIC_REPO_CONTENT = """from sqlmodel import Session, select
from src.config.database import engine
from fastapi import HTTPException

def get_all(model_class):
    with Session(engine) as session:
        return session.exec(select(model_class)).all()

def get_by_id(model_class, id: int):
    with Session(engine) as session:
        item = session.get(model_class, id)
        if not item:
            raise HTTPException(status_code=404, detail=f"{model_class.__name__} not found")
        return item

def create(model_instance):
    with Session(engine) as session:
        session.add(model_instance)
        session.commit()
        session.refresh(model_instance)
        return model_instance

def update(model_class, id: int, new_data):
    with Session(engine) as session:
        db_item = session.get(model_class, id)
        if not db_item:
            raise HTTPException(status_code=404, detail=f"{model_class.__name__} not found")
        for key, value in new_data.dict().items():
            setattr(db_item, key, value)
        session.commit()
        session.refresh(db_item)
        return db_item

def partial_update(model_class, id: int, data: dict):
    with Session(engine) as session:
        db_item = session.get(model_class, id)
        if not db_item:
            raise HTTPException(status_code=404, detail=f"{model_class.__name__} not found")
        for key, value in data.items():
            setattr(db_item, key, value)
        session.commit()
        session.refresh(db_item)
        return db_item

def delete(model_class, id: int):
    with Session(engine) as session:
        item = session.get(model_class, id)
        if not item:
            raise HTTPException(status_code=404, detail=f"{model_class.__name__} not found")
        session.delete(item)
        session.commit()
        return {"success": True}
"""


@task
def scaffold(c, model, fields):
    class_name = model.capitalize()
    model_file = Path(f"src/models/{model}.py")
    controller_file = Path(f"src/controllers/{model}.py")
    route_file = Path(f"src/routes/{model}.py")

    # Criar diretórios
    model_file.parent.mkdir(parents=True, exist_ok=True)
    controller_file.parent.mkdir(parents=True, exist_ok=True)
    route_file.parent.mkdir(parents=True, exist_ok=True)
    GENERIC_REPO_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Criar generic_repository.py se não existir
    if not GENERIC_REPO_PATH.exists():
        GENERIC_REPO_PATH.write_text(GENERIC_REPO_CONTENT)
        print(f"✅ generic_repository.py criado em {GENERIC_REPO_PATH}")

    # Parse dos campos
    parsed_fields = []
    imports = {"str", "int", "float", "bool"}
    for field in fields.split(","):
        parts = field.strip().split(":")
        if len(parts) != 2:
            raise ValueError(f"Campo inválido: '{field}'. Use nome:tipo")
        name, type_ = parts
        parsed_fields.append(f"    {name.strip()}: {type_.strip()}")
        imports.add(type_.strip())

    # model.py
    import_line = "from sqlmodel import SQLModel, Field"
    typing_imports = sorted(imports - {"str", "int", "float", "bool"})
    if typing_imports:
        import_line += f"\nfrom typing import {', '.join(typing_imports)}"

    model_content = f"""{import_line}

class {class_name}(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
{chr(10).join(parsed_fields)}
"""
    model_file.write_text(model_content)
    print(f"✅ Modelo gerado: {model_file}")

    # controller.py chamando repositório genérico
    controller_content = f"""from fastapi import HTTPException
from src.models.{model} import {class_name}
from src.repositories.generic_repository import (
    get_all,
    get_by_id,
    create,
    update,
    partial_update,
    delete,
)

def get_all_controller():
    return get_all({class_name})

def get_by_id_controller(id: int):
    return get_by_id({class_name}, id)

def create_controller(data: {class_name}):
    return create(data)

def update_controller(id: int, data: {class_name}):
    return update({class_name}, id, data)

def partial_update_controller(id: int, data: dict):
    return partial_update({class_name}, id, data)

def delete_controller(id: int):
    return delete({class_name}, id)
"""
    controller_file.write_text(controller_content)
    print(f"✅ Controller gerado: {controller_file}")

    # routes.py com rotas explícitas, sem prefix nem tags
    route_content = f"""from fastapi import APIRouter, Depends
from src.controllers.{model} import (
    get_all_controller,
    get_by_id_controller,
    create_controller,
    update_controller,
    partial_update_controller,
    delete_controller,
)
from src.models.{model} import {class_name}
from src.security.verify_jwt_token import verify_jwt_token

{model}_routes = APIRouter(
    dependencies=[Depends(verify_jwt_token)]
)

@{model}_routes.get("/{model}")
def route_get_all():
    return get_all_controller()

@{model}_routes.get("/{model}/{{id}}")
def route_get_by_id(id: int):
    return get_by_id_controller(id)

@{model}_routes.post("/{model}")
def route_create(data: {class_name}):
    return create_controller(data)

@{model}_routes.put("/{model}/{{id}}")
def route_update(id: int, data: {class_name}):
    return update_controller(id, data)

@{model}_routes.patch("/{model}/{{id}}")
def route_partial_update(id: int, data: dict):
    return partial_update_controller(id, data)

@{model}_routes.delete("/{model}/{{id}}")
def route_delete(id: int):
    return delete_controller(id)
"""
    route_file.write_text(route_content)
    print(f"✅ Rotas geradas: {route_file}")

    # Atualizar src/private_routes.py
    private_routes_file = Path("src/private_routes.py")

    if private_routes_file.exists():
        existing = private_routes_file.read_text()

        import_line = f"from src.routes.{model} import {model}_routes"
        route_entry = f"{model}_routes"

        if import_line not in existing:
            existing = import_line + "\n" + existing

        pattern = r"(private_routes\s*=\s*\[)(.*?)(\])"
        match = re.search(pattern, existing, flags=re.DOTALL)

        if match:
            start, middle, end = match.groups()
            routes = [r.strip() for r in middle.split(",") if r.strip()]
            if route_entry not in routes:
                routes.append(route_entry)
            updated_middle = ", ".join(routes)
            new_routes_block = f"{start}{updated_middle}{end}"
            existing = re.sub(pattern, new_routes_block, existing, flags=re.DOTALL)

            private_routes_file.write_text(existing)
            print(f"✅ private_routes.py atualizado com {model}_routes")
        else:
            print("⚠️  Não foi possível localizar private_routes = [...]")
    else:
        print("⚠️  src/private_routes.py não encontrado.")

    # Formatar com ruff na pasta src usando o comando que funcionou pra você
    try:
        subprocess.run(["ruff", "format", "src"], check=True)
        print("✅ Código formatado com ruff")
    except Exception as e:
        print(f"⚠️ Erro ao formatar código com ruff: {e}")


@task
def destroy(c, model):
    """Remove todos os arquivos gerados por um modelo"""
    paths = [
        Path(f"src/models/{model}.py"),
        Path(f"src/controllers/{model}.py"),
        Path(f"src/routes/{model}.py"),
    ]

    for path in paths:
        if path.exists():
            path.unlink()
            print(f"🗑️ Arquivo removido: {path}")

    # Atualiza o private_routes.py
    private_routes_file = Path("src/private_routes.py")
    if private_routes_file.exists():
        content = private_routes_file.read_text()

        import_line = f"from src.routes.{model} import {model}_routes"
        content = content.replace(import_line + "\n", "")

        pattern = r"(private_routes\s*=\s*\[)(.*?)(\])"
        match = re.search(pattern, content, flags=re.DOTALL)
        if match:
            start, middle, end = match.groups()
            routes = [
                r.strip()
                for r in middle.split(",")
                if r.strip() and r.strip() != f"{model}_routes"
            ]
            updated_middle = ", ".join(routes)
            new_routes_block = f"{start}{updated_middle}{end}"
            content = re.sub(pattern, new_routes_block, content, flags=re.DOTALL)

            private_routes_file.write_text(content)
            print(f"🧹 {model}_routes removido de private_routes.py")

    try:
        subprocess.run(["ruff", "format", "src"], check=True)
        print("✅ Código formatado com ruff")
    except Exception as e:
        print(f"⚠️ Erro ao formatar código com ruff: {e}")
