
# Djanot REST for Recommendation System.

This is an implementation of 
 - [Ultimate Web API Development with Django REST Framework: Build Robust and Secure Web APIs with Django REST Framework Using Test-Driven Development for Data Analysis and Management
Leonardo Luis Lazzaro](https://www.amazon.com/Ultimate-Development-Django-REST-Framework/dp/B0DSHK741V)



## The overview and recommendations.
### Chapter 4
- I have added all_movies file which contains movies, from wikidata including the `year` field(the original file from the book lack of it).Note that after uploading it to your db, you'll get less movie amount, due to duplicates.
- if you would like to download data yourself, include the ["User-Agent"](https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_User-Agent_Policy) header, which increases the 'speed'.
- Increase the `country` CharField's max_length up to 250. Some movies 'have' dozens of countries.
- Don't use `clean_text` function for the `title` field,since some movies has no Latin letters, and would be excluded otherwise.

### Chapter 8
This chapter mainly covers Kubernets and orchestration.
 - To run k8s locally use [minikube](https://minikube.sigs.k8s.io/docs/start/?arch=%2Fmacos%2Farm64%2Fstable%2Fbinary+download). 
 - Use minikube `minikube image load ...`command to mimic the remote(the docker hub).
 - Use `minikube service ..` to connect to your project url.
 - Update the source BEFORE uploading it into Docker Hub for convinice. Otherwise you might have problems with updating the remote and local images' source code.The author uses `docker buildx --platform...` command to build arm64 and amd64 versions. But since your machine only have one architecture it caches the build, i.e it will not be "available".But you are able to push into docker hub and pull it via docker or kubernets with right architecture type implicitly for your local machine,i.e pulling downloads the right platform and the image is 'available'. Now, let's say you have updated your source code and applied the aforementioned command (with --platform flag for several archs.) to update the code in the container, but it will not affect the local active code, since the new build is cached. And since you might already have pulled the image, the pushing will not help, since it will push not the cached version , but the 'active' version. But the active local version is same as you remote version. To solve this problem use --push flag with `docker buildx ` command to instantly push it to Docker Hub. And pull to update the local.
 - Update the env. vars naming in settings.py. The author uses the new env. names(postgres,redis,locals) in kubernets yaml files., but does not mentions it, leading to inconsictency.
 - Use whitenoise python lib to upload static files into your image.  See the Dockerfile and base.py (aka settings.py ). This is also ommmited by the author.
 - The author uses production.py settings , where obviosly the SECRET_KEY is not set.It will be set later in this chapter in k8s conf files, but before you might need to explicilty set in .env file or `export` it to test out things.



## Feedback

Some topics in this book covered and explained well, while other except you to know some basics. Having internet and tons of the online materials mitigates the latter. But `the main problem is in inconsictency`: throughout the book the source code excerpts every now and then conflicts with each other, i.e in some cases the variable names unexpecdely changes or even omitted and etc.And this unfocuses you from development and deep diving into topic, and rather wastes your time fixing supposedly clean code.

Nevertheless, this disadvantage improved my debuggin skills, no cap.

The book must be carefully revised bu authors.


## Authors

- [@llazzaro](https://github.com/llazzaro/django_rest_book/)
- See branches for the source code.
- Note that even the source code is inconsistent. 


