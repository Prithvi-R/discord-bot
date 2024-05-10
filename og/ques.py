import random
import re
import ast
import markdownify
from typing import List

import discord
import requests
from discord.ext import commands

class Questions(commands.Cog):
    def __init__(self, bot: commands.Bot)->None:
        self.bot = bot
        self.logger = self.bot.logger
 
    @commands.command(name="daily", description="Returns the daily problem")
    async def daily(self, ctx: commands.Context):
        url = 'https://leetcode.com/graphql'

        headers = {
            'Content-Type': 'application/json',
        }

        data = {
            'operationName': 'daily',
            'query':
            '''
            query daily {
                challenge: activeDailyCodingChallengeQuestion {
                    date
                    link
                    question {
                        titleSlug
                    }
                }
            }
        '''
        }

        response = requests.post(url, json=data, headers=headers, timeout=10)
        response_data = response.json()
        titleslug = response_data['data']['challenge']['question']['titleSlug']
        {
        # titleslug=response_data['data']['challenge']['question']['title_sweg']

    #     url = 'https://leetcode.com/graphql'
    #     headers = {
    #     'Content-Type': 'application/json',
    #     'Origin': 'https://leetcode.com',
    #     'Referer': 'https://leetcode.com',
    #     'Cookie': 'csrftoken=; LEETCODE_SESSION=;',
    #     'x-csrftoken': '',
    #     'user-agent': 'Mozilla/5.0 LeetCode API'
    #     }
    #     data = {
    #     'operationName': 'questionInfo',
    #     'query':
    #     '''
    #     query questionInfo($titleSlug: String!) {
    #         question(titleSlug: $titleSlug) {
    #             questionFrontendId
    #             title
    #             difficulty
    #             content
    #             likes
    #             dislikes
    #             stats
    #             isPaidOnly
    #         }
    #     }
    #     ''',
    #     'variables': {'titleSlug': titleslug}
    #     }
    #     try:
    #         response = requests.post(url, json=data, headers=headers, timeout=10)

    #     except Exception as e:
    #         self.logger.info(
    #         "file: cogs/questions.py ~ Question could not be retrieved: %s", e)

    #         return

    #     if response.status_code != 200:
    #         self.logger.info(
    #         "file: cogs/questions.py ~ Question could not be retrieved. Error code: %s", response.status_code)

    #         return

    # # Extracting question details from content
    #     response_data = response.json()
    #     difficulty = response_data['data']['question']['difficulty']
    #     question_id = response_data['data']['question']['questionFrontendId']
    #     title = response_data['data']['question']['title']
    #     question_content = response_data['data']['question']['content']
    #     link = f'https://leetcode.com/problems/{titleslug}'
    #     question_stats = ast.literal_eval(
    #         response_data['data']['question']['stats'])
    #     total_accepted = question_stats['totalAccepted']
    #     total_submission = question_stats['totalSubmission']
    #     ac_rate = question_stats['acRate']
    #     premium = response_data['data']['question']['isPaidOnly']

    #     if premium:
    #         return premium, question_id, difficulty, title, link, total_accepted, total_submission, ac_rate, None, None, None

    #     # rating_data = get_rating_data(title)

    #     # question_rating = None
    #     # if rating_data is not None:
    #     #     question_rating = f"||{int(rating_data['rating'])}||"

    #     example_position = question_content.find(
    #         '<strong class="example">')
    #     constraint_query_string = '<p><strong>Constraints:</strong></p>'
    #     constraints_position = question_content.find(constraint_query_string)

    #     description = question_content[:example_position]

    #     constraints = question_content[constraints_position +
    #                                    len(constraint_query_string):]

    #     description = html_to_markdown(description)
    #     constraints = html_to_markdown(constraints)


        # info = get_question_info_from_title(titleslug)

        
        # question_id, difficulty, title, link, total_accepted, total_submission, ac_rate, description, constraints = info

        # color_dict = {"Easy": discord.Color.green(),
        #               "Medium": discord.Color.orange(),
        #               "Hard":  discord.Color.red()}
        # color = color_dict[difficulty] if difficulty in color_dict else discord.Color.blue()

        # # if premium:
        # #     return premium_question_embed(question_id, title, link, color)

        # embed = discord.Embed(
        #     title=f"{question_id}. {title}", url=link, description=description, color=color)

        # embed.add_field(name='Constraints: ', value=constraints, inline=False)

        # embed.add_field(name='Difficulty: ', value=difficulty, inline=True)

        # # if question_rating is not None:
        # #     embed.add_field(name="Zerotrac Rating: ",
        # #                     value=question_rating, inline=True)

        # embed.set_footer(
        #     text=f"Accepted: {total_accepted}  |  Submissions: {total_submission}  |  Acceptance Rate: {ac_rate}")
        }
        
        embed=question_embed(titleslug)

        {
        # # Extract and print the link
        # link = response_data['data']['challenge']['link']
        # # Extract and print the title
        # title = response_data['data']['challenge']['title']
        # # Extract and print the difficulty
        # difficulty = response_data['data']['question']['difficulty']
        # # Extract and print the date
        
        # date = response_data['data']['challenge']['date']
        # link = f"https://leetcode.com{link}"
        # embed = discord.Embed(title=f"Daily Problem: {title}",
        #                       color=discord.Color.blue())
        # embed.add_field(name="**Difficulty**",
        #                 value=f"{difficulty}", inline=True)
        # embed.add_field(name="**Link**", value=f"{link}", inline=False)
        }
        
        self.logger.info(
                f"{ctx.author} asked for daily problem."
            )
        await ctx.send(embed=embed)
        return

    @commands.command(
        name="leetsearch",
        description="Search for any question in leetcode"
    )
    async  def leetsearch(self,ctx:commands.Context,query: str):
        url = 'https://leetcode.com/graphql'
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            'operationName': 'problemsetQuestionList',
            'query':
            '''
            query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
                problemsetQuestionList: questionList(categorySlug: $categorySlug limit: $limit skip: $skip filters: $filters) {
                questions: 
                    data {
                        titleSlug
                    }
                }
            }
            ''',
            'variables': {'categorySlug': "", 'skip': 0, 'limit': 1, 'filters': {'searchKeywords': query}}
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=10)
        response_data = response.json()

        questions_matched_list = response_data['data']['problemsetQuestionList']

        if not questions_matched_list:
            return

        title = questions_matched_list['questions'][0]['titleSlug']
        embed=question_embed(title)
        self.logger.info(
                f"{ctx.author} asked for LeetCode problem search {title}."
            )
        await ctx.send(embed=embed)
        return


    @commands.command(
        name="random",
        description="Request a question based on difficulty or at random")
    async def random(self, ctx: commands.Context, difficulty: str = "random"):
        # if difficulty == "easy":
        #     response = requests.get(
        #         "https://leetcode.com/api/problems/all/", timeout=10)
        #     # Check if the request was successful
        #     if response.status_code == 200:
        #         # Load the response data as a JSON object
        #         data = response.json()

        #         # Get a list of all easy questions from the data
        #         easy_questions = [
        #             question for question in data['stat_status_pairs']
        #             if question['difficulty']['level'] == 1
        #         ]

        #         # Select a random easy question from the list
        #         question = random.choice(easy_questions)

        #         # Extract the question title and link from the data
        #         title = question['stat']['question__title']
        #         link = f"https://leetcode.com/problems/{question['stat']['question__title_slug']}/"

        #         embed = discord.Embed(title="LeetCode Question",
        #                               color=discord.Color.green())
        #         embed.add_field(name="Easy", value=title, inline=False)
        #         embed.add_field(name="Link", value=link, inline=False)

        #         await ctx.send(embed=embed)
        #     else:
        #         # If the request was not successful, send an error message to the Discord channel
        #         self.logger.info(
        #             f"{ctx.author} asked for #{difficulty} level problem but none failed"
        #         )
        #         await ctx.send(
        #             "An error occurred while trying to get the question from LeetCode.")
        #     return
        # elif difficulty == "medium":
        #     response = requests.get(
        #         "https://leetcode.com/api/problems/all/", timeout=10)
        #     # Check if the request was successful
        #     if response.status_code == 200:
        #         # Load the response data as a JSON object
        #         data = response.json()

        #         # Get a list of all medium questions from the data
        #         medium_questions = [
        #             question for question in data['stat_status_pairs']
        #             if question['difficulty']['level'] == 2
        #         ]

        #         # Select a random medium question from the list
        #         question = random.choice(medium_questions)
        #         title = question['stat']['question__title']
        #         link = f"https://leetcode.com/problems/{question['stat']['question__title_slug']}/"

        #         embed = discord.Embed(title="LeetCode Question",
        #                               color=discord.Color.orange())
        #         embed.add_field(name="Medium", value=title, inline=False)
        #         embed.add_field(name="Link", value=link, inline=False)
        #         self.logger.info(
        #             f"{ctx.author} asked for #{difficulty} level problem"
        #         )
        #         await ctx.send(embed=embed)
        #     else:
        #         # If the request was not successful, send an error message to the Discord channel
        #         self.logger.info(
        #             f"{ctx.author} asked for #{difficulty} level problem but failed"
        #         )
        #         await ctx.send(
        #             "An error occurred while trying to get the question from LeetCode.")
        #     return
        # elif difficulty == "hard":
        #     response = requests.get(
        #         "https://leetcode.com/api/problems/all/", timeout=10)
        #     # Check if the request was successful
        #     if response.status_code == 200:
        #         # Load the response data as a JSON object
        #         data = response.json()

        #         # Get a list of all hard questions from the data
        #         hard_questions = [
        #             question for question in data['stat_status_pairs']
        #             if question['difficulty']['level'] == 3
        #         ]

        #         # Select a random hard question from the list
        #         question = random.choice(hard_questions)

        #         title = question['stat']['question__title']
        #         link = f"https://leetcode.com/problems/{question['stat']['question__title_slug']}/"

        #         embed = discord.Embed(title="LeetCode Question",
        #                               color=discord.Color.red())
        #         embed.add_field(name="Hard", value=title, inline=False)
        #         embed.add_field(name="Link", value=link, inline=False)

        #         self.logger.info(
        #             f"{ctx.author} asked for #{difficulty} level problem"
        #         )
        #         await ctx.send(embed=embed)
        #     else:
        #         # If the request was not successful, send an error message to the Discord channel
        #         self.logger.info(
        #             f"{ctx.author} asked for #{difficulty} level problem but failed"
        #         )
        #         await ctx.send(
        #             "An error occurred while trying to get the question from LeetCode.")
        #     return

        # elif difficulty == "random":
            url = requests.get(
                'https://leetcode.com/problems/random-one-question/all').url
        
            embed = discord.Embed(title="Random Question",
                                  color=discord.Color.yellow())
            embed.add_field(name="Link", value=url, inline=False)
            self.logger.info(
                    f"{ctx.author} asked for #{difficulty} level problem"
            )
            await ctx.send(embed=embed)
            return
        



def html_to_markdown(html):
        # Remove all bold, italics, and underlines from code blocks as markdowns doesn't support this.
        html = re.sub(r'(<code>|<pre>)(.*?)(<[/]code>|<[/]pre>)', lambda m: m.group(0).replace('<b>', '').replace('</b>', '').replace(
            '<em>', '').replace('</em>', '').replace('<strong>', '').replace('</strong>', '').replace('<u>', '').replace('</u>', ''), html, flags=re.DOTALL)
    
        subsitutions = [
            (r'<sup>', r'^'),
            (r'</sup>', r''),
            # Replace image tag with the url src of that image
            (r'<img.*?src="(.*?)".*?>', r'\1'),
            (r'<style.*?>.*?</style>', r''),
            (r'&nbsp;', r' ')
        ]
    
        for pattern, replacement in subsitutions:
            html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    
        markdown = markdownify.markdownify(html, heading_style="ATX")
    
        # Remove unnecessary extra lines
        markdown = re.sub(r'\n\n', '\n', markdown)
    
        return markdown

def get_question_info_from_title(titleslug: str) -> List[int | str] | None:
    
        url = 'https://leetcode.com/graphql'
        headers = {
        'Content-Type': 'application/json',
        'Origin': 'https://leetcode.com',
        'Referer': 'https://leetcode.com',
        'Cookie': 'csrftoken=; LEETCODE_SESSION=;',
        'x-csrftoken': '',
        'user-agent': 'Mozilla/5.0 LeetCode API'
        }
        data = {
        'operationName': 'questionInfo',
        'query':
        '''
        query questionInfo($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionFrontendId
                title
                difficulty
                content
                likes
                dislikes
                stats
                isPaidOnly
            }
        }
        ''',
        'variables': {'titleSlug': titleslug}
        }
        try:
            response = requests.post(url, json=data, headers=headers, timeout=10)

        except Exception as e: 
            return

        if response.status_code != 200:
            return
        

    # Extracting question details from content
        response_data = response.json()
        difficulty = response_data['data']['question']['difficulty']
        question_id = response_data['data']['question']['questionFrontendId']
        title = response_data['data']['question']['title']
        question_content = response_data['data']['question']['content']
        link = f'https://leetcode.com/problems/{titleslug}'
        question_stats = ast.literal_eval(
            response_data['data']['question']['stats'])
        total_accepted = question_stats['totalAccepted']
        total_submission = question_stats['totalSubmission']
        ac_rate = question_stats['acRate']

        example_position = question_content.find(
            '<strong class="example">')
        constraint_query_string = '<p><strong>Constraints:</strong></p>'
        constraints_position = question_content.find(constraint_query_string)

        description = question_content[:example_position]

        constraints = question_content[constraints_position +
                                       len(constraint_query_string):]

        description = html_to_markdown(description)
        constraints = html_to_markdown(constraints)
        return question_id, difficulty, title, link, total_accepted, total_submission, ac_rate, description, constraints

def question_embed(question_title: str) -> discord.Embed:
    info = get_question_info_from_title(question_title)

    question_id, difficulty, title, link, total_accepted, total_submission, ac_rate, description, constraints = info

    color_dict = {"Easy": discord.Color.green(),
                  "Medium": discord.Color.orange(),
                  "Hard":  discord.Color.red()}
    color = color_dict[difficulty] if difficulty in color_dict else discord.Color.blue()

    embed = discord.Embed(
        title=f"{question_id}. {title}", url=link, description=description, color=color)

    embed.add_field(name='Constraints: ', value=constraints, inline=False)

    embed.add_field(name='Difficulty: ', value=difficulty, inline=True)

    embed.set_footer(
        text=f"Accepted: {total_accepted}  |  Submissions: {total_submission}  |  Acceptance Rate: {ac_rate}")
    
    return embed

async def setup(bot):
    await bot.add_cog(Questions(bot))
