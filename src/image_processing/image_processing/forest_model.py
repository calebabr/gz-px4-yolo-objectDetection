import torch.nn as nn
import torch.nn.functional as F

# class ForestCNN(nn.Module):
#     def __init__(self, num_classes=2):
#         super(ForestCNN, self).__init__()
#         self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
#         self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
#         self.pool = nn.MaxPool2d(2, 2)
#         self.fc1 = nn.Linear(64 * 32 * 32, 128)
#         self.fc2 = nn.Linear(128, num_classes)

#     def forward(self, x):
#         x = self.pool(F.relu(self.conv1(x)))  # (N, 32, 64, 64)
#         x = self.pool(F.relu(self.conv2(x)))  # (N, 64, 32, 32)
#         x = x.view(-1, 64 * 32 * 32)
#         x = F.relu(self.fc1(x))
#         x = self.fc2(x)
#         return x

class ForestCNN(nn.Module):
    def __init__(self, num_classes):
        super(ForestCNN, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(16, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32 * 32 * 32, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)
        return x