# Brier


The Basic Concept:

This project is based off of Tetlock's Superforecasting (https://goodjudgment.com/). Tetlock's main objective was to find out if people can make predictions about world events, posing questions such as, 'Will Nicolas Maduro cease to be president of Venezuela before 1 April 2021?' and, 'In 2021, will total fire activity in the Amazon exceed the 2020 total count?' (https://www.gjopen.com/questions). After years of research and winning many challenges he came up with a method to make accurate predictions about the future. We will briefly discuss this method here:

1.)Gather a large cohort of people to act as predictors. They will be asked to assign a probability to the chances a world event may or may not happen. Eg. 'There is a 70% chance X will happen.'

2.)Set questions that are falsiable. Eg. 'Will the U.S. consume more energy from renewable sources in May 2021 than it did in May 2019, according to the U.S. Energy Information Administration (EIA)? This question is easy to determine whether the answer is right or wrong compared to, 'Is the US becoming more energy efficient'. Inclusion of a date in the question is key to making it falsifiable.

3.)Once the world event has happened or not by a certain date, now the score of a prediction can be determined. The scoring method used is called a Brier score. A Brier score is calculated as follows: Say one predicts there is a 70% chance something will happen. The event then actually does happen in real life, therefore the probability that it will happen is really 100%. One then takes the difference of the prediction of the event and the real probability of the event and squares it. This value is the score.

  Brier = (f - o)^2
  
  f is the predicted probability
  o is the actual probabilty,  the outcome
  
  (.7 - 1.0)^2 = 0.09 
  
  In this example the prediction receives a score of 0.09 
  
4.) A predictor make many such predictions and each prediction receives a score. Using these individual scores, we calculate the overall score for the predictor themselves.
This can be done using a simple mean average. 
  Eg. A predictor makes two predictions.
    One receives a score of 0.09 and the other 0.25
    The predictors score is (0.09 + 0.25)/2 = 0.17
    
 5.) The overall estimate of the probability of an event is made up of the predictions of every particiant with the predictions coming from those with a low average brier score having a weighted effect on the overall estimate.
 
 This is the method used by tetlock to win IARPA's tornament on the prediction of world events, beating teams from MIT and 
 cf. https://www.iarpa.gov/index.php/working-with-iarpa/prize-challenges/1158-geopolitical-forecasting-challenge-2-gf-challenge-2
 
 This is basic methodology behind what we seek to achieve here.
A Problem of the Modern Day: "The speed of communications is wondrous to behold. It is also true that speed can multiply the distribution of information that we know to be untrue." - Edward R. Murrow

The problem with journalism today is that it is biased and promulgates a certain world view. People and institutions hold these world views because they think that they are an accurate representation of the world and these world views give an ideological tint to everything they see. It is ok to have a theory of how the world works, simplified or otherwise just like with the scientific method: one make observations and develops a theory to explain these observations. Unfortunately, this is where most stop where the scientific method continues. In the scientific method, one uses their theory to generate a prediction from the same principles used to explain the initial observations. One then tests these predictions and, in the words of richard feynman, if the data doesn't agree you're WRONG. How can one apply this to poltical beliefs, theories and world views. If communism explains the world accurately, can it be used to explain what will happen next, do nazis have good insights on house prices? Well we propose that it is with the methodology laid out above.

The predictors with the best scores we assume have the required knowledge and insights of the world to accurately explain why things will happen and why the world is the way it is and what are the key trends to look out for in the future.

The Application: Our webapp routinely propos
