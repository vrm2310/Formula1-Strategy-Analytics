import pandas as pd

# Load datasets

drivers = pd.read_csv("data/raw/drivers.csv")
constructors = pd.read_csv("data/raw/constructors.csv")
races = pd.read_csv("data/raw/races.csv")
results = pd.read_csv("data/raw/results.csv")
qualifying = pd.read_csv("data/raw/qualifying.csv")
circuits = pd.read_csv("data/raw/circuits.csv")

print("Drivers:", drivers.shape)
print("Constructors:", constructors.shape)
print("Races:", races.shape)
print("Results:", results.shape)
print("Qualifying:", qualifying.shape)
print("Circuits:", circuits.shape)

print("\nMissing Values\n")

datasets = {
    "drivers": drivers,
    "constructors": constructors,
    "races": races,
    "results": results,
    "qualifying": qualifying,
    "circuits": circuits
}

for name, df in datasets.items():
    print(f"\n{name.upper()}")
    print(df.isnull().sum())

for name, df in datasets.items():
    print(f"\n{name.upper()} COLUMNS")
    print(df.columns.tolist())

drivers["driver_name"] = (
    drivers["forename"] + " " + drivers["surname"]
)

drivers_clean = drivers[
    ["driverId", "driver_name", "nationality"]
]

constructors_clean = constructors[
    ["constructorId", "name", "nationality"]
]

constructors_clean = constructors_clean.rename(
    columns={
        "name": "constructor_name",
        "nationality": "constructor_nationality"
    }
)

circuits_clean = circuits[
    [
        "circuitId",
        "name",
        "location",
        "country"
    ]
]

circuits_clean = circuits_clean.rename(
    columns={
        "name": "circuit_name"
    }
)

races_clean = races[
    [
        "raceId",
        "year",
        "round",
        "circuitId",
        "name",
        "date"
    ]
]

races_clean = races_clean.rename(
    columns={
        "name": "race_name"
    }
)

races_clean["date"] = pd.to_datetime(
    races_clean["date"]
)

results_clean = results[
    [
        "raceId",
        "driverId",
        "constructorId",
        "grid",
        "positionOrder",
        "points",
        "laps",
        "fastestLap"
    ]
]

qualifying_clean = qualifying[
    [
        "raceId",
        "driverId",
        "position"
    ]
]

qualifying_clean = qualifying_clean.rename(
    columns={
        "position": "qualifying_position"
    }
)

# Merge results with drivers

f1_df = results_clean.merge(
    drivers_clean,
    on="driverId",
    how="left"
)

print(f1_df.shape)

f1_df = f1_df.merge(
    constructors_clean,
    on="constructorId",
    how="left"
)

print(f1_df.shape)

f1_df = f1_df.merge(
    races_clean,
    on="raceId",
    how="left"
)

print(f1_df.shape)

f1_df = f1_df.merge(
    circuits_clean,
    on="circuitId",
    how="left"
)

print(f1_df.shape)

f1_df = f1_df.merge(
    qualifying_clean,
    on=["raceId", "driverId"],
    how="left"
)

print(f1_df.shape)

print(f1_df.head())
print(f1_df.info())

f1_df.to_csv(
    "data/processed/f1_analytics_dataset.csv",
    index=False
)

print(f1_df.columns.tolist())

print(
    f1_df.groupby("year")["qualifying_position"]
         .count()
         .sort_index()
)

print(f1_df["fastestLap"].head(20))

print(f1_df["fastestLap"].unique()[:20])

print(f1_df.isnull().sum())

# Remove unnecessary column

f1_df = f1_df.drop(
    columns=["fastestLap"]
)

f1_df.to_csv(
    "data/processed/f1_analytics_dataset.csv",
    index=False
)

print(f1_df["positionOrder"].describe())
print(f1_df["grid"].describe())