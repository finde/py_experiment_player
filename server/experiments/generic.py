import json
from logging import root
import random
from fastapi import APIRouter

import os
from natsort import natsorted, ns
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.requests import Request
from server.sensor import universal_marker
from server.core.config import settings as config
from fastapi.encoders import jsonable_encoder

# MODEL
from pydantic import BaseModel


class RatingAnswer(BaseModel):
    experiment_id: str
    block_name: str
    name: str
    value: float


class CompositeRatingAnswer(BaseModel):
    experiment_id: str
    block_name: str
    name: str
    value: dict


class Experiment:
    def __init__(self, experiment_id):
        root_dir = f"{config.EXP_ROOT_DIR}/{experiment_id}"
        router = APIRouter()

        self.router = router
        self.root_dir = root_dir
        self.templates_dir = f"{root_dir}/{config.EXP_TEMPLATE_DIR}"
        self.assets_dir = f"{root_dir}/{config.EXP_ASSETS_DIR}"
        self.output_dir = f"{root_dir}/{config.EXP_OUTPUT_DIR}"

        self.setup_router(router)

    def get_router(self):
        return self.router

    def _load_block_template_metadata(self, template_file):
        data = {}
        try:
            with open("{}/{}.json".format(self.templates_dir, template_file)) as f:
                data = json.load(f)

        except:
            print("Can't load {}".format(template_file))

        return data

    def block_questionnaire(self, config, name="questionnaire", template_file="questionnaire"):
        data = self._load_block_template_metadata(template_file)
        data["type"] = "sequence"
        data["name"] = name

        for k, v in enumerate(data["items"]):
            if v["type"] == "rating":
                data["items"][k]["block_name"] = name

        return data

    def block_basic(
        self,
        config,
        name="basic",
        type="sequence",
        template_file="basic"
    ):
        data = self._load_block_template_metadata(template_file)
        data["type"] = type
        data["name"] = name
        return data

    def experiment(self, config):

        # load from config
        experiment_blocks = []
        items = []

        experiment_id = config["experiment_id"]
        cache_file = f"_cache_{experiment_id}.json"

        # load cache if exists
        if os.path.exists(cache_file):
            with open("{}/{}".format(self.output_dir, cache_file)) as fp:
                print("cache exists, load session")
                cache_output = json.load(fp)
                return cache_output

        print("cache not exists, create new session")
        with open("{}/config.json".format(self.root_dir)) as fp:
            settings = json.load(fp)
            experiment_blocks = settings["experiment_blocks"]

        for block in experiment_blocks:
            if "is_random" in block:
                block["template_file"] = random.choice(block["template_file"])
                print(block["template_file"])

            if block["type"] in ["sequence", "intro", "closing"]:
                items.append(
                    self.block_basic(
                        config,
                        name=block["name"],
                        type=block["type"],
                        template_file=block["template_file"]
                    )
                )

            elif block["type"] == "questionnaire":
                items.append(
                    self.block_questionnaire(
                        config=config,
                        name=block["name"],
                        template_file=block["template_file"]
                    )
                )                

        output = {"type": "experiment", "items": items}

        for key, value in dict(config).items():
            if isinstance(value, str):
                output[key] = value.lower()
            else:
                output[key] = value

        with open("{}/{}".format(self.output_dir, cache_file), "w") as fp:
            json.dump(output, fp, indent=1, sort_keys=True)

        return output

    ## ROUTER
    def setup_router(self, router):
        @router.get("/check")
        async def check():
            data = {"code": 200}
            return JSONResponse(content=data)

        @router.post("/request-new-id")
        async def generate_new_id():
            files = [
                f
                for f in os.listdir(self.output_dir)
                if os.path.isfile(os.path.join(self.output_dir, f) and not f.startswith('.'))
            ]

            data = {"id": "0001"}

            if len(files) > 0:
                files.sort()
                data["id"] = "{:04d}".format(int(files[-1].replace(".json", "")) + 1)

            return JSONResponse(content=data)

        @router.post("/create")
        async def create_experiment(request: Request):
            settings = await request.form()
            settings = jsonable_encoder(settings)

            data = {"isOk": True, "experiment_id": settings["experiment_id"]}

            with open(
                "{}/{}.json".format(self.output_dir, settings["experiment_id"]), "w"
            ) as fp:
                json.dump(settings, fp, indent=1, sort_keys=True)

            return JSONResponse(content=data)

        @router.post("/rating-answer")
        async def handle_rating_answer(answer: RatingAnswer):
            data = {}

            with open("{}/{}.json".format(self.output_dir, answer.experiment_id)) as fp:
                data = json.load(fp)

            with open(
                "{}/{}.json".format(self.output_dir, answer.experiment_id), "w"
            ) as fp:
                data["{}##{}".format(answer.block_name, answer.name)] = answer.value
                json.dump(data, fp, indent=1, sort_keys=True)

            data = {
                "isOk": True,
            }
            return JSONResponse(content=data)

        @router.post("/composite-rating-answer")
        async def handle_composite_rating_answer(answer: CompositeRatingAnswer):
            data = {}
            with open("{}/{}.json".format(self.output_dir, answer.experiment_id)) as fp:
                data = json.load(fp)

            with open(
                "{}/{}.json".format(self.output_dir, answer.experiment_id), "w"
            ) as fp:
                data["{}".format(answer.name)] = answer.value
                json.dump(data, fp, indent=1, sort_keys=True)

            data = {
                "isOk": True,
            }
            return JSONResponse(content=data)

        @router.get("/marker/{code}")
        async def record_marker(code):
            print(f"sending marker {code}")
            universal_marker(code)
            return f"Marker code {code}"

        @router.post("/get-config")
        async def get_experiment_settings():
            settings = {}
            with open("{}/config.json".format(self.root_dir)) as fp:
                settings = json.load(fp)

            return JSONResponse(content=settings)

        @router.post("/{exp_id}")
        async def create_or_reload(exp_id):
            settings = {}
            with open("{}/{}.json".format(self.output_dir, exp_id)) as fp:
                settings = json.load(fp)

            data = self.experiment(settings)
            return JSONResponse(content=data)

        @router.get("/", response_class=HTMLResponse)
        @router.get("/{session_id}", response_class=HTMLResponse)
        async def homepage(request: Request):
            return config.TEMPLATES.TemplateResponse("index.html", {"request": request})