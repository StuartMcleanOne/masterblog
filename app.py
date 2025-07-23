from flask import Flask, render_template, request, redirect, url_for # url_for dynamically builds URLS by using view function names like index
import json
import os

app = Flask(__name__)
DATA_FILE = "blog_posts.json"

def load_posts():
    """
    Load blog posts from the JSON file.
    :return:
        list: A list of dictionaries, where each dictionary represents a blog post.
    """
    #Check if the file exists before trying to open it to avoid errors.
    if os.path.exists(DATA_FILE):
        with open("blog_posts.json","r") as file:
            return json.load(file)
    return [] # If the file doesn't exist yet, return empty list.

def save_posts(posts):
    """
    Save rhe updated list of blog posts to the JSON file.
    :param posts: (list): the updated list of a blog post dictionaries to be saved.

    """
    # Write the list of posts into the file.
    with open(DATA_FILE, "w") as file:
        json.dump(posts, file, indent=4)

@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Handle GET and POST requests for add a new blog post.
    :return: GET: Show the form for creating a blog post.
             POST: Add the submitted data as tha new blog post to JSON file.
    """
    if request.method == "POST":
        # Extract form data sent by the user.
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Load current list of posts from file.
        posts = load_posts()

        # Generate a unique ID by finding the highest existing ID.
        next_id = max([post["id"] for post in posts], default=0) + 1

        # Create a dictionary for the new post.
        new_post = {
            "id": next_id,
            "author": author,
            "title": title,
            "content": content
        }

        # Add the new post to the list.
        posts.append(new_post)

        # Save the updated list back to the JSON file.
        save_posts(posts)

        # Redirect user to homepage after successful post creation.
        return redirect(url_for('index'))

    # If its a get request, show the blank form to the user.
    return render_template('add.html')

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """
    Delete a blog post by its unique ID.

    This function is triggeredwhen the user accesses the delete/post_id.
    It reads the JSON file of blog posts, filters out the post with the given ID,
    saves the updated list, and redirects the user to the home page.

    :param post_id (int): The unique identifier of the blog post to remove.
    :return: Response object: Redirects to the home page showing the updated list.
    # Post method prevents accidental deletions.
    # Forms trigger POST so its more intentional.
    """

    # Load existing blog posts as a list of dictionaries
    posts = load_posts()

    #Filter out the post with the matching ID.
    updated_posts = [post for post in posts if post["id"] != post_id] # removes the dictionary you want to delete

    # Save the new list back to the JSON file.
    save_posts(updated_posts)

    # Redirect user back to the home page to view updated posts
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Handle the update of specific blog post.

    GET: Display the form populated with existing post data.
    POST: Apply the changes from the form and update the post in the JSON file.

    :param:
        Post_id(int): The unique ID of the blog post to edit.

    :return:
        Redirect to index page after update or render form for editing.
    """
    posts = load_posts()

    # Find the posts that we're editing.
    post = next((p for p in posts if p["id"] == post_id), None)

    if not post:
        return "Post not found", 404

    if request.method == "POST":
        # Update the posts fields with form data.
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')

        # Save the updated post list
        save_posts(posts)
        return redirect(url_for('index'))

    # Render update form with exisiting post data
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)