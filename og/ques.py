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
        
        embed=question_embed(titleslug)

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
