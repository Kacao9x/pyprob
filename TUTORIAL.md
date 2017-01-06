# Tutorial for Compiled Inference

## Table of Contents
- [Dependencies](#dependencies)
    - [Manual](#manual)
    - [Docker Image](#docker-image)
- [I just want to break Captchas...](#i-just-want-to-break-captchas)
- [Writing the Probabilistic Program](#writing-the-probabilistic-program)
- [Compilation](#compilation)
- [Inference](#inference)

## Dependencies
### Manual
- [Clojure](http://clojure.org/guides/getting_started): Anglican runs on Clojure.
- [Leiningen](http://leiningen.org/#install): Package manager for Clojure programs.
- [Anglican CSIS](https://github.com/tuananhle7/anglican-csis): Required for the CSIS extensions of Anglican (will be moved to Clojars soon)
```
$ git clone https://github.com/tuananhle7/anglican-csis.git
$ cd anglican-csis
$ lein install
```
- [Torch](http://torch.ch/docs/getting-started.html)
- [Torch Autograd](https://github.com/twitter/torch-autograd#install)
- Torch packages via [LuaRocks](https://luarocks.org/):
```
$ luarocks install ansicolors
$ luarocks install cephes
$ luarocks install hash
$ luarocks install https://raw.github.com/jucor/torch-distributions/master/distributions-0-0.rockspec
$ luarocks install lzmq
$ luarocks install lua-messagepack
$ luarocks install rnn
```

### Docker Image

## I just want to break Captchas

Download one of the artifacts and unzip it to the `data/` folder:
- [Wikipedia Captcha](TODO)
- [Facebook Captcha](TODO)

From the root folder of this repository, run
```
th infer.lua --cuda --artifact data/wikipedia --model data/wikipedia.clj
```

## Writing the Probabilistic Program
### Setting up Leiningen Project
Include the dependencies for [Anglican](http://www.robots.ox.ac.uk/~fwood/anglican/index.html) and the Compiled Sequential Importance Sampling (CSIS) backend in your Leiningen `project.clj` file:
```
:dependencies [...
               [anglican "1.0.0"]
               [anglican-csis "0.1.0-SNAPSHOT"]
               ...])
```

In your Clojure file, remember to `require` the following in order to be able to define Anglican queries and perform inference using CSIS:
```
(:require ...
          anglican.csis.csis
          [anglican.csis.network :refer :all]
          [anglican.inference :refer [infer]]
          ...)
(:use [anglican emit runtime])
```

## Compilation
After you've defined your probabilistic program in [Anglican language](http://www.robots.ox.ac.uk/~fwood/anglican/language/index.html), you can compile it. The typical workflow consists of these steps:

1. **Define a function to combine observes.**
Specify a function `combine-observes-fn` (you can name it anything) that combines observes from a sample in a form suitable for Torch. This will be used in the next step when starting the Clojure-Torch connection. In order to write this function, you'll need to look at how a typical `observes` object from your query looks like. This can be done by running `(sample-observes-from-prior q q-args)` where `q` is your query name and `q-args` are the arguments to the query.
2. **Start a Clojure-Torch [ZeroMQ](http://zeromq.org/) connection from the Clojure side.** Use `start-torch-connection` function in Clojure ([docs](http://tuananhle.co.uk/anglican-csis-doc/anglican.csis.network.html#var-start-torch-connection)). Remember to bind this to a variable which will be used later to stop this connection. E.g. `(def torch-connection (start-torch-connection q q-args combine-observes-fn))`.
3. **Train the neural network in Torch.** `cd` to the root folder and run `th compile.lua`. Run `th compile.lua --help` to see and possibly override default options.
4. **Stop the training of the neural network.** This can be done by `Ctrl+C` from the terminal. How long should I train? There aren't any theoretical bounds for the loss. If all your random variables are discrete, the minimum should be around 0. Otherwise, just iterate between Compilation and Inference.
5. **Stop the Clojure-Torch ZeroMQ connection.** To stop the Clojure-Torch server from Clojure, use the previously bound `torch-connection`. E.g. `(stop-torch-connection torch-connection)`.

## Inference
After you've compiled your query by training up a neural network, you can perform inference using the Compiled Sequential Importance Sampling algorithm. You will hopefully need much fewer particles in comparison to Sequential Monte Carlo to perform inference. The typical workflow consists of these steps:

1. **Run inference from Clojure.** `cd` to the root folder and run `th infer.lua`. Run `th infer.lua --help` to see and possibly override default options. Stop this process by `Ctrl+C` after you're done performing inference in Clojure in the next step.
2. **Evaluate inference in Clojure.** To get 10 particles from the CSIS inference algorithm, run
```
(def num-particles 10)
(def csis-states (take num-particles (infer :csis q q-args)))
(take 10 csis-states)
```