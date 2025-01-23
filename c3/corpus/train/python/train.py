import json
import torch
from torch.utils.data import Dataset, DataLoader 
import torch.nn as nn
import torch.optim as optim
import time

with open("../json/vocab.json", "r", encoding="utf-8") as f:
    vocab = json.load(f)

if not vocab:
    raise Exception("Error: vocab file not loaded properly")
print("vocab loaded")
class EncodedDataset(Dataset):
    def __init__(self, file_path, vocab):
        self.sentences = []
        self.vocab = vocab
        with open(file_path, "r") as f:
             self.sentences = [json.loads(line.strip()) for line in f]

    def __len__(self):
        return len(self.sentences) 

    def __getitem__(self, idx):
        sentence = self.sentences[idx]
        input_ids = torch.sensor(sentence[:-1], dtype=torch.long)
        label = torch.sensor(sentence[-1], dtype=torch.long)
        return input_ids, label

    #TODO: getitems?

batch_size = 32

print("encoding datasets")
train_dataset = EncodedDataset("../json/data/train_data.jsonl", vocab)
print("encoded training data")
val_dataset = EncodedDataset("../json/data/val_data.jsonl", vocab)
print("encoded validation data")
test_dataset = EncodedDataset("../json/data/test_data.jsonl", vocab)
print("encoded testing data")

print("initializing dataloaders")
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
print("training loaded")
val_loader = DataLoader(val_dataset, batch_size=batch_size)
print("validation loaded")
test_loader = DataLoader(test_dataset, batch_size=batch_size)
print("testing loaded")

#TODO: byte-wise tokenization?
class SimpleLSTMModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim):
        super(SimpleLSTMModel, self).__init__() #TODO: ??
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0) 
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        embedded = self.embedding(x)
        lstm_out, (hidden, _) = self.lstm(embedded)
        output = self.fc(hidden[-1])
        return output

vocab_size = len(vocab) 
embedding_dim = 100
hidden_dim = 120
output_dim = vocab_size

model = SimpleLSTMModel(vocab_size, embedding_dim, hidden_dim, output_dim)


# Define loss function and optimizer
criterion = nn.CrossEntropyLoss()  
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training Loop
print("starting training")
epochs = 5
for epoch in range(epochs):
    model.train()
    epoch_loss = 0
    for batch_idx, (inputs, labels) in enumerate(train_loader):
        batch_start_time = time.time()
        optimizer.zero_grad()
        predictions = model(inputs)
        loss = criterion(predictions, labels)

        loss.backward() # TODO: ??
        optimizer.step() # TODO: ??

        epoch_loss += loss.item()

        #TODO: better time estimation (average batches?)
        batch_time = time.time() - batch_start_time
        remaining_batches = len(train_loader) - (batch_idx + 1)
        remaining_time = remaining_batches * batch_time
        print(f"Epoch {epoch + 1}/{epochs}, Batch {batch_idx + 1}/{len(train_loader)}, "
              f"Batch Time: {batch_time:.2f}s, Estimated Time Remaining: {remaining_time:.2f}s")

        
    print(f"Epoch {epoch + 1}/{epochs}, Loss: {epoch_loss:.4f}")

#TODO: add saving
#Use a library like tqdm for a visual progress bar that includes timing.
