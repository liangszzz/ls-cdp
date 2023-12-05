from src.main.cdp.common.options import WriteOptions
from src.main.cdp.utils.glue_utils import export_df_to_csv_file, get_glue_context
from src.main.cdp.utils.s3_utils import check_s3_file_or_dir_exist


def test_get_glue_context():
    context = get_glue_context()
    assert context is not None


def test_export_df_to_csv_file(glue_context, s3):
    df = glue_context.sparkSession.createDataFrame([("Alice", 1)], "name string,age int")

    export_df_to_csv_file(df, "cdp-output1", "path/1.csv", WriteOptions.csv_options.value)
    assert check_s3_file_or_dir_exist(s3, "cdp-output1", "path/1.csv", False)
