# Overview

This repository is designed for revising Python fundamentals and exploring advanced topics, including:

- **Python Built-in Functions (BIFs)**
- **Standard Library modules**
- **Popular PyPI packages**
- [**Deployment using *PythonAnywhere* and *Azure***](#deployment)

All content is referenced from the *Head First Python* ebook, making it a practical guide for both beginners and experienced Python developers.

Use this repository to:
- Review core Python concepts
- Deep dive into essential libraries and tools
- Practice with examples and exercises

<br>

<hr> <span style="color: green; padding-left: 15rem;"><b>Happy coding!</b></span> <hr>

<br>

## Deployment
*Always dreaded this part. But the book made it smoother than expected!* 

- Both the cloud services require an account. 
- I am currently using only free-tier or free account wherever possible.


### Using PythonAnywhere
1. Zip the `app/` directory
2. In the website, use *WebApps* feature
3. Upload to *Files* 
4. Open a Bash console and unzip `app.zip`
4. Update `WSGI` (pronounced '*whiskey*' apparently!) to point at the correct `app.py`
5. Force enable HTTPS security
  - After setting these up, reload the website on the platform
6. Voila! App deployed.

> [Visit PythonAnywhere endpoint](https://hfpy.pythonanywhere.com/)


### Using Azure Developer CLI
1. Install Azure Developer CLI extension in VS Code
2. Create a new project directory for the infrastructure files (apparently a big deal!)
3. Using VS Code Command Palette, initialize app or `azd init` using terminal (after IDE restart) by choosing a template to deploy a simple Flask app
  - The initializtion (`init`) process set up the resources (`resource-group`), infrastructure files, sample app and a brief documentation of how to get going with *azd*
4. Zip `app/` and move it to new directory 
5. Run `azd up` (= `azd auth login` + `azd package` + `azd provision` + `azd deploy`) in terminal
  - This command might run a while since it performs several complex tasks (my deployment completed under 4 mins)
  - Downloads `Bicep` for setting up the infrastructure
  - Provisions the resources, services based on *Subscription* and *Location*
  - Finally deploys the app!

*PS. Always check for `requirements.txt` to have only essential frameworks/libraries for fast and error-free deployment*

> [Visit Azure endpoint](https://web-q4lmqh7s5jbm4.azurewebsites.net/)
