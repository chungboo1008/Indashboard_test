import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Categorical
import ipdb
import random



class biRNN_Net(nn.Module):
    def __init__(self, voc_size, emb_size, tag_size, weights, projection_size=512):
        super(biRNN_Net, self).__init__()
        self.voc_size = voc_size
        self.emb_size = emb_size
        self.tag_size = tag_size
        self.projection_size = projection_size
        self.h_size = 128
        
       
        
        # self.word_embeddings  = nn.Embedding(voc_size, emb_size)
        self.word_embeddings  = nn.Embedding.from_pretrained(weights)
        self.rnn_1 = nn.LSTM(input_size = emb_size, hidden_size = self.h_size*4, batch_first=True, bidirectional=True)
        self.linear_1 = nn.Linear(self.h_size*2*4, projection_size)
        self.rnn_2 = nn.LSTM(input_size = projection_size, hidden_size = self.h_size*4, batch_first=True, bidirectional=True)
        self.linear_2 = nn.Linear(self.h_size*2*4, projection_size)
        self.hidden2tag = nn.Linear(projection_size, tag_size)
        self.dropout = torch.nn.Dropout(0.5)
        


    def forward(self, sentence):
    
        embeds = self.word_embeddings(sentence) # (16, 200, 300)
        lstm_out, _ = self.rnn_1(embeds, None) # (16, 200, 512)
        lstm_out = self.dropout(lstm_out)    
        lstm_out = self.linear_1(lstm_out)
        lstm_out = self.dropout(lstm_out)  
        lstm_out, _ = self.rnn_2(lstm_out, None)
        lstm_out = self.dropout(lstm_out)    
        lstm_out = self.linear_2(lstm_out)
        lstm_out = self.dropout(lstm_out)
        tag_space = self.hidden2tag(lstm_out)  # (16, 200, 2)
        # tag_scores = F.log_softmax(tag_space, dim=1) # (16, 200, 2)
        
        return tag_space

    def predict(self, sentence):
        """
        Args:
            given: (1, sent_len)
            tags:  (1, sent_len)
            skip_word_indices: [indices of special tokens: BOS, PAD, UNK]
        """

        x = self.word_embeddings(sentence)       # (batch, p_len, emb_size)  # (1,2,300)
        lstm_out, _ = self.rnn_1(x, None) # (16, 200, 256)
        lstm_out = self.dropout(lstm_out)    
        lstm_out = self.linear_1(lstm_out)
        lstm_out = self.dropout(lstm_out)
        lstm_out, _ = self.rnn_2(lstm_out, None)
        lstm_out = self.dropout(lstm_out)    
        lstm_out = self.linear_2(lstm_out)
        lstm_out = self.dropout(lstm_out)
        tag_space = self.hidden2tag(lstm_out)  # (16, 200, 2)

        return tag_space
        