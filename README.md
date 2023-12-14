# langIDFserver (cc by 4.0)
langIDFserver

# Details

https://docs.google.com/document/d/1VTCtqLbeoe3BODB1MRaO2Evfr8_mYASQaxRLa5URXaM/edit?usp=sharing

## Schema details

https://github.com/ULCA-IN/ulca/blob/develop/specs/model-schema.yml

## Supported language classes (Indian Languages only)

["as","bho","bn","en","gu","hi","kn","ml","mni","mr","or","pa","ta","te","ur","unk"]


# How to Run

## Install Modules

sudo apt-get install docker-compose

## Build Docker image

sudo docker build -t lang-server . 

## Run Docker image

sudo docker run -p 8046:8046 lang-server

## How to do inference


```
POST URL : http://0.0.0.0:8046/langidentify

JSON INPUT (ULCA) :

{
    "input": [
        {
            "source": "કોરોનાને કારણે છેલ્લાં બે વર્ષથી ગરબાનું આયોજન થઈ શક્યું નહોતું"
        },
        {
            "source": "my name is sachin"
        }
    ]
}

```
```
JSON OUTPUT (ULCA) :

{
    "output": [
        {
            "langPrediction": [
                {
                    "langCode": "gu",
                    "langScore": 100
                }
            ],
            "source": "કોરોનાને કારણે છેલ્લાં બે વર્ષથી ગરબાનું આયોજન થઈ શક્યું નહોતું"
        },
        {
            "langPrediction": [
                {
                    "langCode": "en",
                    "langScore": 100
                }
            ],
            "source": "my name is sachin"
        }
    ]
}

```


## Owner/Contect
1. Vandan Mujadia (vandan.mu@research.iiit.ac.in)
2. Dipti M Sharma (dipti@iiit.ac.in)
