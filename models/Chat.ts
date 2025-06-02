import mongoose from 'mongoose';

const messageSchema = new mongoose.Schema({
  content: { type: String, required: true },
  role: { type: String, required: true, enum: ['user', 'assistant'] },
  createdAt: { type: Date, default: Date.now }
});

const chatSchema = new mongoose.Schema({
  title: { type: String, required: true },
  userId: { type: String, required: true },
  messages: [messageSchema],
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
});

// Update the updatedAt timestamp before saving
chatSchema.pre('save', function(next) {
  this.updatedAt = new Date();
  next();
});

export const Chat = mongoose.models.Chat || mongoose.model('Chat', chatSchema); 