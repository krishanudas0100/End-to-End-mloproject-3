"""
Kubeflow Pipeline for End-to-End ML Project (mlproject3)
=========================================================
Mirrors the 5-stage main.py:
  Stage 1 – Data Ingestion
  Stage 2 – Data Validation
  Stage 3 – Data Transformation
  Stage 4 – Model Training
  Stage 5 – Model Evaluation

Prerequisites
-------------
1. Build & load a Docker image that contains your src/mlproject3 package:
      docker build -t mlproject3:latest .
      kind load docker-image mlproject3:latest --name <your-kind-cluster-name>

2. Create a Kubernetes Secret for MLflow credentials (one-time):
      kubectl create secret generic mlflow-secret \
        --from-literal=MLFLOW_TRACKING_URI=https://dagshub.com/krishanudas0100/End-to-End-mloproject-3.mlflow \
        --from-literal=MLFLOW_TRACKING_USERNAME=krishanudas0100 \
        --from-literal=MLFLOW_TRACKING_PASSWORD=<YOUR_TOKEN> \
        -n kubeflow          # ← change to your KF namespace

3. Compile this file:
      python mlproject3_kubeflow_pipeline.py

4. Upload the generated mlproject3_pipeline.yaml via the Kubeflow UI
   (Pipelines → Upload pipeline) or with the KFP SDK:
      kfp.Client(host="http://127.0.0.1:8080").create_run_from_pipeline_package(
          "mlproject3_pipeline.yaml", arguments={}
      )
"""

import kfp
from kfp import dsl
from kfp import kubernetes
from kfp.dsl import PipelineTask

# ──────────────────────────────────────────────────────────────
# CONFIG  –  change these two values before compiling
# ──────────────────────────────────────────────────────────────
BASE_IMAGE = "mlproject3:latest"   # ← your Docker image (loaded into kind)
MLFLOW_SECRET = "mlflow-secret"                    # ← K8s secret name
# ──────────────────────────────────────────────────────────────


def _add_mlflow_env(task: PipelineTask) -> PipelineTask:
    """
    Inject MLflow credentials from a Kubernetes Secret into any component.
    Keeps credentials out of source code and pipeline YAML.
    Uses the kfp-kubernetes extension (pip install kfp-kubernetes).
    """
    kubernetes.use_secret_as_env(
        task,
        secret_name=MLFLOW_SECRET,
        secret_key_to_env={
            "MLFLOW_TRACKING_URI": "MLFLOW_TRACKING_URI",
            "MLFLOW_TRACKING_USERNAME": "MLFLOW_TRACKING_USERNAME",
            "MLFLOW_TRACKING_PASSWORD": "MLFLOW_TRACKING_PASSWORD",
        },
    )
    return task


# ──────────────────────────────────────────────────────────────
# STAGE 1 – Data Ingestion
# ──────────────────────────────────────────────────────────────
@dsl.component(base_image=BASE_IMAGE)
def data_ingestion_component() -> str:
    """
    Runs DataIngestionTrainingPipeline and returns a status string.
    The component re-uses the exact same class you already have in
    src/mlproject3/pipeline/data_ingestion_pipeline.py
    """
    from src.mlproject3 import logger
    from src.mlproject3.pipeline.data_ingestion_pipeline import DataIngestionTrainingPipeline

    STAGE_NAME = "Data Ingestion Stage"
    try:
        logger.info(f">>>>> {STAGE_NAME} started <<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.initiate_data_ingestion()
        logger.info(f">>>> stage {STAGE_NAME} Completed <<<<")
        return "success"
    except Exception as e:
        logger.exception(e)
        raise


# ──────────────────────────────────────────────────────────────
# STAGE 2 – Data Validation
# ──────────────────────────────────────────────────────────────
@dsl.component(base_image=BASE_IMAGE)
def data_validation_component(ingestion_status: str) -> str:
    """
    Runs DataValidationTrainingPipeline.
    'ingestion_status' input creates an explicit dependency edge
    so Kubeflow executes stages in the correct order.
    """
    from src.mlproject3 import logger
    from src.mlproject3.pipeline.data_validation_pipeline import DataValidationTrainingPipeline

    STAGE_NAME = "Model Validation Stage"
    try:
        logger.info(f">>>>> {STAGE_NAME} started <<<<<")
        obj = DataValidationTrainingPipeline()
        obj.initiate_data_validation()
        logger.info(f">>>> stage {STAGE_NAME} Completed <<<<")
        return "success"
    except Exception as e:
        logger.exception(e)
        raise


# ──────────────────────────────────────────────────────────────
# STAGE 3 – Data Transformation
# ──────────────────────────────────────────────────────────────
@dsl.component(base_image=BASE_IMAGE)
def data_transformation_component(validation_status: str) -> str:
    """
    Runs DataTransformationTraingPipeline.
    """
    from src.mlproject3 import logger
    from src.mlproject3.pipeline.data_transformation_pipeline import DataTransformationTraingPipeline

    STAGE_NAME = "Model Transformation Stage"
    try:
        logger.info(f">>>>> {STAGE_NAME} started <<<<<")
        obj = DataTransformationTraingPipeline()
        obj.initiate_data_transformation()
        logger.info(f">>>> stage {STAGE_NAME} Completed <<<<")
        return "success"
    except Exception as e:
        logger.exception(e)
        raise


# ──────────────────────────────────────────────────────────────
# STAGE 4 – Model Training
# ──────────────────────────────────────────────────────────────
@dsl.component(base_image=BASE_IMAGE)
def model_trainer_component(transformation_status: str) -> str:
    """
    Runs ModelTrainerTrainingPipeline.
    MLflow tracking credentials are injected via K8s Secret (see pipeline def).
    """
    from src.mlproject3 import logger
    from src.mlproject3.pipeline.model_trainer_pipeline import ModelTrainerTrainingPipeline

    STAGE_NAME = "Model Trainer Stage"
    try:
        logger.info(f">>>>> {STAGE_NAME} started <<<<<")
        obj = ModelTrainerTrainingPipeline()
        obj.initiate_model_training()
        logger.info(f">>>> stage {STAGE_NAME} Completed <<<<")
        return "success"
    except Exception as e:
        logger.exception(e)
        raise


# ──────────────────────────────────────────────────────────────
# STAGE 5 – Model Evaluation
# ──────────────────────────────────────────────────────────────
@dsl.component(base_image=BASE_IMAGE)
def model_evaluation_component(training_status: str) -> str:
    """
    Runs ModelEvaluationTrainingpipeline.
    MLflow tracking credentials are injected via K8s Secret (see pipeline def).
    """
    from src.mlproject3 import logger
    from src.mlproject3.pipeline.model_evalutation_pipeline import ModelEvaluationTrainingpipeline

    STAGE_NAME = "Model Evaluation Stage"
    try:
        logger.info(f">>>>> {STAGE_NAME} started <<<<<")
        obj = ModelEvaluationTrainingpipeline()
        obj.initiate_model_evaluation()
        logger.info(f">>>> stage {STAGE_NAME} Completed <<<<")
        return "success"
    except Exception as e:
        logger.exception(e)
        raise


# ──────────────────────────────────────────────────────────────
# PIPELINE DEFINITION
# ──────────────────────────────────────────────────────────────
@dsl.pipeline(
    name="end-to-end-mlproject3-pipeline",
    description=(
        "5-stage ML pipeline: Data Ingestion → Validation → "
        "Transformation → Training → Evaluation. "
        "MLflow credentials injected from a Kubernetes Secret."
    ),
)
def mlproject3_pipeline():

    # --- Stage 1: Data Ingestion ---
    ingestion_task = data_ingestion_component()
    ingestion_task = _add_mlflow_env(ingestion_task)
    ingestion_task.set_display_name("Stage 1 - Data Ingestion")
    kubernetes.set_image_pull_policy(ingestion_task, "IfNotPresent")

    # --- Stage 2: Data Validation (depends on Stage 1) ---
    validation_task = data_validation_component(
        ingestion_status=ingestion_task.output
    )
    validation_task = _add_mlflow_env(validation_task)
    validation_task.set_display_name("Stage 2 - Data Validation")
    kubernetes.set_image_pull_policy(validation_task, "IfNotPresent")

    # --- Stage 3: Data Transformation (depends on Stage 2) ---
    transformation_task = data_transformation_component(
        validation_status=validation_task.output
    )
    transformation_task = _add_mlflow_env(transformation_task)
    transformation_task.set_display_name("Stage 3 - Data Transformation")
    kubernetes.set_image_pull_policy(transformation_task, "IfNotPresent")

    # --- Stage 4: Model Training (depends on Stage 3) ---
    training_task = model_trainer_component(
        transformation_status=transformation_task.output
    )
    training_task = _add_mlflow_env(training_task)
    training_task.set_display_name("Stage 4 - Model Training")
    # Give the trainer more CPU/RAM if needed
    training_task.set_cpu_request("200m")
    training_task.set_cpu_limit("500m")
    training_task.set_memory_request("512Mi")
    training_task.set_memory_limit("1Gi")
    kubernetes.set_image_pull_policy(training_task, "IfNotPresent")

    # --- Stage 5: Model Evaluation (depends on Stage 4) ---
    evaluation_task = model_evaluation_component(
        training_status=training_task.output
    )
    evaluation_task = _add_mlflow_env(evaluation_task)
    evaluation_task.set_display_name("Stage 5 - Model Evaluation")
    kubernetes.set_image_pull_policy(evaluation_task, "IfNotPresent")


# ──────────────────────────────────────────────────────────────
# COMPILE  →  mlproject3_pipeline.yaml
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    output_file = "mlproject3_pipeline.yaml"

    kfp.compiler.Compiler().compile(
        pipeline_func=mlproject3_pipeline,
        package_path=output_file,
    )
    print(f"✅ Pipeline compiled successfully → {output_file}")

    # ── Optional: submit directly to a running Kubeflow instance ──
    # client = kfp.Client(host="http://127.0.0.1:8080")
    # run = client.create_run_from_pipeline_func(
    #     mlproject3_pipeline,
    #     arguments={},
    #     run_name="mlproject3-run-v1",
    # )
    # print(f"🚀 Run submitted: {run.run_id}")