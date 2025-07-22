const books =[
    {title: "The Shawshank Redemption", author: "Stephen King", 
        year: 1982, description: "A story of hope and resilience in a bleak prison environment."},
    {title: "The Godfather", author: "Mario Puzo", 
        year: 1969, description: "An organized crime dynasty's aging patriarch transfers control of his clandestine empire to his reluctant son."},
    {title: "The Dark Knight", author: "Jonathan Nolan", 
        year: 2008, description: "When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham."},
    {title: "The great Gatsby", author: "F. Scott Fitzgerald", 
        year: 1925, description: "A story of the mysteriously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan."},
    {title: "1984", author: "George Orwell", 
        year: 1949, description: "A dystopian social science fiction novel and cautionary tale about the dangers of totalitarianism."},
    {title: "To Kill a Mockingbird", author: "Harper Lee", 
        year: 1960, description: "A novel about the serious issues of race and class in the Deep South."},
    {title: "Pride and Prejudice", author: "Jane Austen",
        year: 1813, description: "A romantic novel that charts the emotional development of the protagonist, Elizabeth Bennet."},
    {title: "The Catcher in the Rye", author: "J.D. Salinger",
        year: 1951, description: "A story about teenage angst and alienation, narrated by the cynical Holden Caulfield."}
]

const booksContainer = document.getElementById("booksContainer");

books.forEach(book => {
    const card = document.createElement("div");
    card.className = "book-card";

    const title = document.createElement("h2");
    title.textContent = book.title;

    const author = document.createElement("p");
    author.textContent = `Author: ${book.author}`;

    const year = document.createElement("p");
    year.textContent = `Year: ${book.year}`;

    const description = document.createElement("p");
    description.textContent = `Description: ${book.description}`;

    card.appendChild(title);
    card.appendChild(author);
    card.appendChild(year);
    card.appendChild(description);
    booksContainer.appendChild(card);
});