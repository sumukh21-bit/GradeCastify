# preprocessing and training code for the MLP

from MLP import *
from torch.utils.data import DataLoader, TensorDataset
import matplotlib.pyplot as plt
import sklearn.metrics as metrics
import sklearn.model_selection as model_selection
import sklearn.preprocessing as preprocessing
from sklearn.utils.class_weight import compute_class_weight

df = pd.read_csv("ML/data/studentperformancedata.csv")

# clean the data and prepare features for training
df = df.dropna()
df["current_avg"] = df.apply(calculate_current_avg, axis=1)

# create the feature matrix and target vector
X = df.loc[:, ["Sleep_Hours_per_Night", "Stress_Level (1-10)", "Attendance (%)", "Department", "current_avg"]].values
y = df["Grade"].map(grade_map).values

# split into training and test sets
y_tensor = torch.tensor(y, dtype=torch.long)
X_train, X_test, y_train, y_test = model_selection.train_test_split(
    X, y_tensor, test_size=0.1, random_state=42, stratify=y_tensor
    )

# normalize features  and convert to tensors
scaler = preprocessing.StandardScaler()
X_train = torch.tensor(scaler.fit_transform(X_train), dtype=torch.float32)
X_test = torch.tensor(scaler.transform(X_test), dtype=torch.float32)



# create datasets and dataloaders
train_dataset = TensorDataset(X_train, y_train)
test_dataset = TensorDataset(X_test, y_test)

train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_dataloader = DataLoader(test_dataset, batch_size=32, shuffle=False)

# initialize the model
input_size = X.shape[1]
hidden_size = 64
output_size = len(set(y))
model = MLP(input_size, hidden_size, output_size)

# train the model
logger = pl.loggers.CSVLogger("ML/lightning_logs", name="mlp")
trainer = pl.Trainer(max_epochs=50, logger=logger, enable_checkpointing=False)
trainer.fit(model, train_dataloader)
torch.save(model.state_dict(), "ML/artifacts/mlp.pt")

# get predictions and calculate metrics
model.eval()
with torch.no_grad():
    preds = model(X_test)
    preds = torch.argmax(preds, dim=1).numpy()

print("Classification Report:")
print(metrics.classification_report(y_test, preds, target_names=grade_map.keys()))

# plot loss
log_data = pd.read_csv("ML/lightning_logs/mlp/version_0/metrics.csv")
plt.plot(log_data["train_loss"].dropna().values, label="Train Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Training Loss")
plt.legend()
plt.savefig("ML/artifacts/loss_plot.png")