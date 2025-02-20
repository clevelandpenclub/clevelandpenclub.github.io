Hey, it's Amelorate.
I wrote the backbones of the website you're reading now.
Unfortunately, I've got severe programmer-brain, so a lot of the things on this website don't really work the way you'd expect.
For those in the know, the magic words are this is a Static Site hosted on [Github](https://github.com/clevelandpenclub/clevelandpenclub.github.io) [Pages](https://pages.github.com).
Comments are done using [Giscus](https://giscus.app).

For the rest of you, you're the target audience of this guide.

# How The Website Is Made

You don't really need to understand this part of the article to follow the other sections below, but [todo write the rest later]

# Comments Sections

To leave a comment, just click the Sign In With Github button, authorize the app, and you should be able to write your comment.
If you don't have a Github account, you'll be given the opportunity to create one.
The other parts of this guide will also prompt you to either sign into your account or create one when it's needed.

## How To Get An Email When Someone Comments

If you really want to be involved, you can sign up to be emailed whenever anyone comments on an article or has something to say about the website.

In order to do so, first [click this link to navigate to the website's Github Repository.](https://github.com/clevelandpenclub/clevelandpenclub.github.io)
Then, you'll click the 👁️Watch button near the top right of your screen.

There's a few options for how many emails you'll get: 
* All Activity will send you an email whenever anyone comments, makes changes to the website, proposes changes to the website, or really does anything related to the website.
* Custom lets you select which things will email you.
  * We use Issues for things that are to-do.
    For example, if there's a bug with the website or something that's incomplete, we'd create an issue.
    Suggestions for articles to write would also be an issue.
   * Pull Requests are suggestions for changes to the website that someone's already written.
     For example, if someone's written an article for us that'll be a Pull Request.
   * The last feature that we use are Discussions.
     When you make a comment on an article, it'll create a discussion and reply to it with that comment.
     However, there is a sour point: If someone reacts to an article that has zero reactions and zero comments, it'll send you an annoying and confusing email.
     Sorry, this can't be fixed.
     I wish I could, but it's one of those things where everyone you complain to points the finger at someone else.
     In the first place, there's nobody to complain to because nobody's being paid for any of this.

![Arrow pointing to the Watch button](/assets/CommentTutorial1.png)

--

![Dropdown that appears when you click the Watch button](/assets/CommentTutorial2.png)

--

![Options popup when you click Custom](/assets/CommentTutorial3.png)

# Creating a Post

You may have noticed the [Make a new post](/tools/new-post.html) link on the main page.
Unsuprisingly, this is the first part of making a new post.
Simply fill in the title of your article, and if the date of the article isn't today you can change it using the date selector.
If your title has special characters, you'll have to copy and paste the section of code at the **beginning** of your post or else the special characters will be removed.
Also, if you want your post to have a comment section, you can click the checkbox.
You'll have to paste that section of code at the **end** of your post for it to work.
Then, click *Next*.

If you've got access to edit the website directly, then you'll just be able to write your article in the box.
If you don't have access, you'll have to click the *Fork this repository* button, and then you'll be able to write it.
Forking a repositiory is like making a copy of the website onto computer so you can make changes to it.
However, instead of your computer it'll be copied to Github's computers instead.

Once you've got the editing screen open, you can write your post here in [Github Flavored Markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).
You can find a [quick reference for Markdown here.](https://gist.github.com/Myndex/5140d6fe98519bb15c503c490e713233)
Markdown is a way of writing documents that allows you to use plain text in any editor to create a web page.
If you've ever used WordPerfect or WordStar for Microsoft DOS, it's kind of like that.

Make sure to credit yourself at the end of your article by writing something like `--Amelorate`.

Once you've written your article, you should click *Commit changes...*, and then *Commit changes*/*Propose changes* in the popup.
You don't really need to change the Commit message or the description if it's for a new article.
The default message is good enough.

If you've got access to edit the website directly, then you're done!
If you don't then you've got to continue on to create a Pull Request, which is a formal request to make a change to the website.
Just click *Create pull request*, and then once again click *Create pull request* on the new screen.
Amelorate will get an email and he'll put your changes online soon.

In terms of copyright, the Cleveland Pen Club website is licensed under [Creative Commmons Zero.](https://creativecommons.org/public-domain/cc0/)
This means that the webite, everything written on it, and all its pictures entirely lack copyright and are in the Public Domain.
If this is a problem, you could include a different license at the bottom of the article you've written as long as the Cleveland Pen Club and Github are allowed to distriute the file and make changes as needed.

## Editing Existing Posts

The website's posts are stored in the [_posts folder](https://github.com/clevelandpenclub/clevelandpenclub.github.io/tree/main/_posts) in Github.
You can edit a post by clicking the post you want to edit, and then clicking the pencil icon in the top left corner.
Once you're done, hit *Commit changes...*, and give it a message describing which post you're editing and what kind of a change you've made in one sentence.
Additional details about your changes can be added in the description.
Then, just do the same thing you did with Creating a Post in terms of clicking *Commit changes* if you have access or *Propose changes* if you don't.

![Arrow pointing to the edit button](/assets/EditTutorial.png)

## Editing Other Pages

On the top bar of the website, there's pages like Sophants, Specimines, Story, and so on.
These are kept in the [base folder of ther website's Github](https://github.com/clevelandpenclub/clevelandpenclub.github.io), and they can be edited much like posts.
Files that end in `.md` are pages that you can edit.
Files that don't end in `.md` are important for keeping the website working.
You might want to avoid touching those.

Most of the pages here are pretty simple, but there are a few complications.
* `README.MD` is the home page of the website.
* `sophants.md` and `specimines.md` are both really complicated:
  Both of these pages use a data-driven approach, where all of their actual content is stored in the [_data folder.](https://github.com/clevelandpenclub/clevelandpenclub.github.io/tree/main/_data)
  If you know how to edit YAML, feel free to edit this.
  If you don't, don't feel obligated to learn it.
  Just ask Amelorate, and she'll take care of it.

{% include cle-comments.md %}
