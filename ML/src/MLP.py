# simple MLP model for student grade forecasting using pytorch lightning
# also includes functions and definition of maps for training preparation

import torch
import torch.nn as nn
import pytorch_lightning as pl
import pandas as pd
import numpy as np

class MLP(pl.LightningModule):
    def __init__(self, input_size, hidden_size, output_size):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size // 2)
        self.fc3 = nn.Linear(hidden_size // 2, output_size)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):
        out = self.dropout(self.relu(self.fc1(x)))
        out = self.dropout(self.relu(self.fc2(out)))
        out = self.fc3(out)
        return out
    
    def training_step(self, batch, batch_idx):
        x, y = batch
        preds = self(x)
        loss = nn.CrossEntropyLoss()(preds, y)
        self.log('train_loss', loss, on_step=False, on_epoch=True)
        return loss
    
    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=0.001)
        return optimizer
    
# function to calculate current average while ignoring N/A values
def calculate_current_avg(row):
    # ASSUMPTION THAT ALL COMPONENTS ARE EQUALLY WEIGHTED
    # IF A USER HAS N/A FOR ANY COMPONENT, EXCLUDE IT FROM THE CALCULATION OF THE AVERAGE
    components = [row["Midterm_Score"], row["Assignments_Avg"],
                  row["Quizzes_Avg"], row["Participation_Score"]]
    applicable = [i for i in components if pd.notna(i)]
    if len(applicable) > 0:
        return np.mean(applicable)
    else:
        return 0

# define integer mappings for categorical variables
grade_map = {"A": 4, "B": 3, "C": 2, "D": 1, "F": 0}
major_map = {"Mathematics": 0, "CS": 1, "Engineering": 2, "Business": 3}