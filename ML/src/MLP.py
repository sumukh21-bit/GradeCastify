# simple MLP model for student grade forecasting using pytorch lightning
# also includes functions and definition of maps for training preparation

import torch
import torch.nn as nn
import pytorch_lightning as pl
import pandas as pd
import numpy as np



class MLP(pl.LightningModule):
    def __init__(self, input_size, hidden_size, output_size, class_weights=None):
        super(MLP, self).__init__()

        self.layer = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Linear(hidden_size // 2, output_size),
        
         

        )
        self.dropout = nn.Dropout(0.3)
        self.loss_fn = nn.CrossEntropyLoss(weight=class_weights)
    def forward(self, x):
        out = self.dropout(self.dropout((self.layer(x))))
        
        return out
    
    def training_step(self, batch):
        x, y = batch
        preds = self(x)
        loss = self.loss_fn(preds, y)
        self.log('train_loss', loss)
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
