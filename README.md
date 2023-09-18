# Fabled Fusion

This project is my expirement in using ChatGPT to write and power a web application. This is meant to be an AI powered Pokemon clone where each montster encountered is unique in its type and imagae. I used ChatGPT to make templates that would be generated sent into the Dalle API. The ChatGPT API is used to generate adventures for the monsters to go on.

## Take away

I was impressed how fast I was able to itterate on this project. Yeeting code and vague descriptions of code into ChatGPT was surprisingly effective in generating working code. The point at which this failed me is when I started asking for different configurations for an app running locally and running in production. ChatGPT just wasnt able to hold the full context of all the Django backend, NextJS frontend, NGINX, and Dockerfiles for two separate versions of a project. While it is super useful for debugging such a large file it wasn't able to generate two working configurations. It got confused on what I had working and where the errors were.

## Future ideas

I would like to expirement with using the ChatGPT API and a parser to look through my code, build contexts, and send it through ChatGPT. I think this could help keep the over all context accurate with each query I make to get new code.

## Ultimate goal
What I really want to accomplish here is to build an interactive game that gives uses the power to create and express their imagination with the power of an LLM and Stable Diffusion. Creataing characters, images of those character, and story lines will be a fun way to teach the user how to use AI. It will be a visual programming language for AI; a sort of AI templating engine.

This will all start within the confines of this game, but will become a platform where other usecases can be implemented. For instance I would like to create a template for a web application that allows users to create a robust web app that can be deployed both locally and in production with a few simple queries.
