from flask import Flask, render_template, request, redirect
import uuid
import pymongo
import datetime

app = Flask(__name__)

# database connection setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["blog_post"]
blogs = db["blogs"]


@app.route("/", methods=["GET", "POST"])
def blog():
    if request.method == "POST":
        result = blogs.find(
            {
                "title": request.form.get("title")
            },
            {"_id": 0, },
        ).sort(
            [("title", pymongo.ASCENDING)]
        )
        return render_template("blog.html", result=result)

    result = blogs.find(
        {},
        {"_id": 0, },
    ).sort(
        [("title", pymongo.ASCENDING)]
    )
    return render_template("blog.html", result=result)


@app.route("/create", methods=["GET", "POST"])
def blogCreate():
    if request.method == "POST":
        blog = {
            "_id": uuid.uuid4().hex,
            "title": request.form.get("title"),
            "body": request.form.get("body"),
        }
        if (len(blog["title"]) > 5 and len(blog["body"]) > 10):
            blogs.insert_one(blog)
            return redirect("/", code=302)
        else:
            return render_template("blogCreate.html", error="Please fill all the fields")
    return render_template("blogCreate.html")


@app.route("/update/<title>", methods=["GET", "POST"])
def blogInfo(title):
    result = blogs.find_one(
        {
            "title": title
        },
        {"_id": 0, },
    )
    if request.method == "POST":
        if (len(request.form.get("title")) > 5 and len(request.form.get("body")) > 10):
            blogs.update_one(
                {"title": title},
                {
                    "$set": {
                        "title": request.form.get("title"),
                        "body": request.form.get("body"),
                    }
                },
            )
            return redirect("/", code=302)
        else:
            return render_template("blogUpdate.html", result=result, error="Please fill all the fields")

    return render_template("blogUpdate.html", result=result, error="")


@app.route("/delete/<title>")
def blogDelete(title):
    blogs.delete_one(
        {
            "title": title
        }
    )
    return redirect("/", code=302)

@app.route("/details/<title>")
def blogDetails(title):
    result = blogs.find_one(
        {
            "title": title
        },
        {"_id": 0, },
    )
    return render_template("blogDetails.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
