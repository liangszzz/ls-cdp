from enum import Enum


class ReadOptions(Enum):
    csv_options = {
        "header": "true",
        "encoding": "utf-8",
        "quote": '"',
        "escape": '"',
    }

    tsv_options = {
        "header": "true",
        "encoding": "utf-8",
        "quote": '"',
        "escape": '"',
        "sep": "\t",
    }

    parquet_options = {
        "encoding": "utf-8",
    }

    fixed_options = {
        "header": "false",
        "encoding": "utf-8",
    }


class WriteOptions(Enum):
    csv_options = {
        "header": "true",
        "quote": '"',
        "escape": '"',
        "quoteAll": "true",
        "compression": "gzip",
    }

    tsv_options = {
        "header": "true",
        "encoding": "utf-8",
        "quote": '"',
        "escape": '"',
        "quoteAll": "true",
        "compression": "gzip",
    }

    parquet_options = {"compression": "gzip"}

    txt_options = {"header": "true", "encoding": "utf-8", "compression": "gzip"}

    fixed_options = {"header": "false", "encoding": "utf-8", "compression": "gzip"}
