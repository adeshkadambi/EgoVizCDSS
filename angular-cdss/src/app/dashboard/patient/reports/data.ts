export const test_val = {
    "name": new Date('June 6, 2021'),
    "value": Math.floor(Math.random()*100)
}

export const multi = [
    {
      "name": "Right Hand",
      "series": [
        {
            "name": new Date('June 1, 2021'),
            "value": Math.floor(Math.random()*100)
        },
        {
            "name": new Date('June 3, 2021'),
            "value": Math.floor(Math.random()*100)
        },
        {
            "name": new Date('June 5, 2021'),
            "value": Math.floor(Math.random()*100)
        },
        {
            "name": new Date('June 7, 2021'),
            "value": Math.floor(Math.random()*100)
        },
        {
            "name": new Date('June 9, 2021'),
            "value": Math.floor(Math.random()*100)
        }
      ]
    },
  
    {
      "name": "Left Hand",
      "series": [
        {
            "name": new Date('June 1, 2021'),
            "value": Math.floor(Math.random()*100)
        },
        {
            "name": new Date('June 3, 2021'),
            "value": Math.floor(Math.random()*100)
        },
        {
            "name": new Date('June 5, 2021'),
            "value": Math.floor(Math.random()*100)
        },
        {
            "name": new Date('June 7, 2021'),
            "value": Math.floor(Math.random()*100)
        },
        {
            "name": new Date('June 9, 2021'),
            "value": Math.floor(Math.random()*100)
        }
      ]
    }
];

export const minutes_recorded = [
    {
        "name": "06/01",
        "value": 32,
    },
    {
        "name": "06/03",
        "value": 256,
    },
    {
        "name": "06/04",
        "value": 144,
    },
    {
        "name": "06/05",
        "value": 168,
    },
    {
        "name": "06/07",
        "value": 248,
    },
    {
        "name": "06/09",
        "value": 96,
    },
    {
        "name": "06/10",
        "value": 144,
    },
    {
        "name": "06/12",
        "value": 168,
    },
    {
        "name": "06/13",
        "value": 32,
    },
    {
        "name": "06/14",
        "value": 256,
    },
    {
        "name": "06/16",
        "value": 144,
    },
    {
        "name": "06/17",
        "value": 168,
    },
    {
        "name": "06/18",
        "value": 248,
    },
    {
        "name": "06/20",
        "value": 96,
    },
    {
        "name": "06/23",
        "value": 144,
    },
    {
        "name": "06/26",
        "value": 168,
    },
];

export const patient_notes = [
    {
        date: new Date(2021, 5, 5),
        note: "felt pain in my right arm."
    },
    {
        date: new Date(2021, 5, 12),
        note: "preparing food was more difficult than usual."
    },
    {
        date: new Date(2021, 5, 5),
        note: "felt pain in my right arm."
    },
    {
        date: new Date(2021, 5, 12),
        note: "preparing food was more difficult than usual."
    },
    {
        date: new Date(2021, 5, 16),
        note: "camera stopped recording."
    },
    {
        date: new Date(2021, 5, 5),
        note: "felt pain in my right arm."
    },
    {
        date: new Date(2021, 5, 12),
        note: "preparing food was more difficult than usual."
    },
    {
        date: new Date(2021, 5, 16),
        note: "camera stopped recording."
    },
];

export const activity_breakdown = [
    {
        "name": "Cook",
        "value": "60",
        "extra": {
            "Top Posture": "Posture 1",
            "Tenodesis Grasp": "Yes",
        }
    },
    {
        "name": "Eat",
        "value": "10",
        "extra": {
            "Top Posture": "Posture 2",
            "Tenodesis Grasp": "No",
        }
    },
    {
        "name": "Clean",
        "value": "10",
        "extra": {
            "Top Posture": "Posture 3",
            "Tenodesis Grasp": "No",
        }
    },
    {
        "name": "Misc",
        "value": "20",
        "extra": {
            "Top Posture": "Posture 4",
            "Tenodesis Grasp": "Yes",
        }
    },
];
  
export const posture_use = [
    {
      "name": "6/01",
      "series": [
        {
          "name": "Power Grasp",
          "value": 70
        },
        {
          "name": "Intermediate",
          "value": 10
        },
        {
          "name": "Precision Grasp",
          "value": 20
        },
      ]
    },
    {
      "name": "6/03",
      "series": [
        {
          "name": "Power Grasp",
          "value": 65
        },
        {
          "name": "Intermediate",
          "value": 15
        },
        {
          "name": "Precision Grasp",
          "value": 20
        },
      ]
    },
    {
      "name": "6/04",
      "series": [
        {
          "name": "Power Grasp",
          "value": 45
        },
        {
          "name": "Intermediate",
          "value": 30
        },
        {
          "name": "Precision Grasp",
          "value": 25
        },
      ]
    },
    {
      "name": "6/05",
      "series": [
        {
          "name": "Power Grasp",
          "value": 45
        },
        {
          "name": "Intermediate",
          "value": 15
        },
        {
          "name": "Precision Grasp",
          "value": 40
        },
      ]
    },
];

export const postures = [
  {
    name: "Power Grasp",
    image: "pretend this is an image",
  },
  {
    name: "Intermediate",
    image: "pretend this is an image",
  },
  {
    name: "Precision Grasp",
    image: "pretend this is an image",
  },
];