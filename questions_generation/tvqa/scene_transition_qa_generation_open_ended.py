import os 
import re
import json 
import ast 
import random
# set the seed for reproducibility 
random.seed(72) # it is my birthday 7th of February
from tqdm import tqdm
MCQ_header="Choose the correct option for the following question: "
pool_of_questions=[
    "what is the correct squence of scene transition in this episode?",
    "Can you outline the order of scene changes in this episode?",
    "What is the correct sequence of scene transitions in this episode?",
    "Could you detail the progression of scenes in this episode?",
    "How do the scenes transition in this episode?",
    "What is the chronological order of scenes in this episode?",
    "Can you describe the sequence of events in the episode?",
    "What order do the scenes appear in this episode?",
    "How are the scenes organized in this episode?",
    "Could you list the scenes in the order they occur in this episode?",
    "What is the sequence of scene shifts in this episode?",
]

ann_paths=[
    "../../skills_output/tvqa/scene_transitions/friends.json",
    "../../skills_output/tvqa/scene_transitions/bbt.json",
    "../../skills_output/tvqa/scene_transitions/met.json",
    "../../skills_output/tvqa/scene_transitions/grey.json",
    "../../skills_output/tvqa/scene_transitions/house.json",
    "../../skills_output/tvqa/scene_transitions/castle.json"
]
 
benchmark_data=[]  

def generate_open_ended_answers(list_of_transotions):
    answer_str="Then scene is transitioned from "
    for transition in list_of_transotions:
        answer_str+=transition+" to "
    return answer_str[:-4]


existed_episodes=json.load(open("../../analysis/existed_videos_tvqa.json",'r'))
print("Number of existed episodes: ", len(existed_episodes))
print("existed episodes: ", existed_episodes)
for ann_path in tqdm(ann_paths):
    with open (ann_path,'r') as f:
        scene_transitions=json.load(f)

    show_name=ann_path.split('/')[-1].split('.')[0]
    for episode in scene_transitions:
        transitions_list=scene_transitions[episode]
        if show_name=="friends":
            name_list=episode.split('__')
            season=name_list[0]
            episode=name_list[1]
        else:
            season="season_"+str(int(episode.split('_')[2]))
            episode="episode_"+str(int(episode.split('_')[4]))
        if f"/{show_name}/{season}/{episode}" not in existed_episodes:
            continue
        correct_answer=transitions_list.copy()
        open_ended_answers=generate_open_ended_answers(transitions_list)
        
        random_q=random.choice(pool_of_questions)
        question=random_q
        data={}
        data['question']=question
        data['answer']=open_ended_answers
        data['show']=show_name
        data['season']=season
        data['episode']=episode
        data['source']="tvqa"
        data['video_path_mp4']=f"/{show_name}/{season}/{episode}.mp4"
        data['video_path_frames']=f"/{show_name}/{season}/{episode}"
        data['video_subtitles']=f"/{show_name}/{season}/{episode}.srt"  
        benchmark_data.append(data)
os.makedirs("../../benchmark",exist_ok=True)
with open('../../benchmark/scene_transitions_benchmark_open_ended.json','w') as f:
    json.dump(benchmark_data,f)
        
        
        
        
        
        
        