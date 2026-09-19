main <- function() {
  tracking_uri <- Sys.getenv("MLFLOW_TRACKING_URI", unset = "")
  if (!grepl("^http://127\\.0\\.0\\.1:[0-9]+/?$", tracking_uri)) {
    stop("Set MLFLOW_TRACKING_URI to an approved local demo server on 127.0.0.1")
  }
  if (!requireNamespace("mlflow", quietly = TRUE)) {
    stop("Install the project's compatible R mlflow package and Python MLflow environment first")
  }
  mlflow::mlflow_set_tracking_uri(tracking_uri)
  mlflow::mlflow_set_experiment("skill-r-tracking")
  mlflow::mlflow_start_run()
  succeeded <- FALSE
  on.exit(mlflow::mlflow_end_run(status = if (succeeded) "FINISHED" else "FAILED"), add = TRUE)
  set.seed(42)
  feature <- seq(-2, 2, length.out = 100)
  dataset <- data.frame(feature = feature, target = 2 * feature + rnorm(100, sd = 0.2))
  train_ids <- sample(seq_len(nrow(dataset)), size = 80)
  model <- stats::lm(target ~ feature, data = dataset[train_ids, ])
  heldout <- dataset[-train_ids, ]
  prediction <- stats::predict(model, newdata = heldout)
  rmse <- sqrt(mean((prediction - heldout$target)^2))
  mlflow::mlflow_log_param("seed", 42)
  mlflow::mlflow_log_param("purpose", "synthetic-single-model-smoke")
  mlflow::mlflow_log_param("r_version", as.character(getRversion()))
  mlflow::mlflow_log_param("r_mlflow_version", as.character(utils::packageVersion("mlflow")))
  mlflow::mlflow_log_metric("test_rmse", rmse)
  session_path <- tempfile(pattern = "r-session-", fileext = ".txt")
  on.exit(unlink(session_path), add = TRUE)
  writeLines(capture.output(utils::sessionInfo()), session_path)
  mlflow::mlflow_log_artifact(session_path)
  succeeded <- TRUE
  message("Local R tracking smoke completed; no model was registered or deployed")
}

main()
