const mongoose = require('mongoose');

const bookSchema = new mongoose.Schema({
  bookId: String,
  bookLink: String,
  bookTitle : String,
  bookRate: String,
  bookDescription: String,
  bookReviews: {
    userId: [String],
    userName : [String],
    rate: [Number],
    contentReview: [String],
    commentList: [String],
    datePost: [String],
  }
});

const Book = mongoose.model('Book', bookSchema);

module.exports = Book;
