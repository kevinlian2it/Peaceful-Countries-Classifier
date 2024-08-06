'''
Code for finding DOI of references of Fry article
'''
import requests
import os
from dotenv import load_dotenv
load_dotenv()

def parse_input(input_str):
    """
    Parses the input string to extract the title and author.

    Args:
        input_str (str): The input string containing the title and author.

    Returns:
        tuple: A tuple containing the title and author.
    """
    title = input_str.split(', Author:')[0].replace('Title: ', '').strip()
    author = input_str.split(', Author:')[1].strip()
    return title, author


def find_doi_scopus(title, author, api_key):
    query = f'TITLE({title}) AND AUTH({author})'
    url = f'https://api.elsevier.com/content/search/scopus?query={query}&apiKey={api_key}&field=doi'

    response = requests.get(url)
    if response.status_code == 200 and response.json().get('search-results').get('entry'):
        try:
            doi = response.json()['search-results']['entry'][0].get('prism:doi', 'DOI not found')
            if doi != 'DOI not found':
                return doi
        except IndexError:
            pass
    return None


def find_doi_wos(title, author, api_key):
    url = "https://wos-api.clarivate.com/api/woslite/"
    headers = {'X-ApiKey': api_key}
    params = {
        'databaseId': 'WOS',
        'usrQuery': f'TI=({title}) AND AU=({author})',
        'count': '1',
        'firstRecord': '1'
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200 and response.json().get('Data').get('Records').get('records'):
        try:
            doi = \
            response.json()['Data']['Records']['records']['REC'][0]['dynamic_data']['cluster_related']['identifiers'][
                'identifier'][0]['value']
            return doi
        except (IndexError, KeyError, TypeError):
            pass
    return None

dois = []
remain = []
def find_doi(input_str):
    scopus_api_key = os.environ.get("elsevier")
    #wos_api_key = 'your_wos_api_key'

    title, author = parse_input(input_str)

    # Try Scopus first
    doi = find_doi_scopus(title, author, scopus_api_key)
    if doi:
        return doi
    #else:
        #doi = find_doi_wos(title, author, wos_api_key)
        #if doi:
            #dois.append(doi)
    remain.append([title, author])
    return


strings = ["Title: Intergroup violence and political attitudes: evidence from a dividing Sudan, Author: Beber, B", 'Title: Intergroup violence and intergroup attributions, Author: Hunter, J. A', 'Title: Reciprocity\'s dark side: Negative reciprocity, morality and social reproduction, Author: Narotzky, Susana.', 'Title: Intergroup Anxiety, Author: Stephan, Walter', 'Title: No lessons learned from the Holocaust? Assessing risks of genocide and political mass murder since 1955, Author: Harff, B.', 'Title: RETURNING THE GIFT—UTU IN INTERGROUP RELATIONS: In memory of Sir Raymond Firth, Author: Metge, Joan.', 'Title: The UN and Regional Organizations in Global Security: Competing or Complementary Logics?, Author: Hettne, Bjorn.', 'Title: UN Early Warning for Preventing Conflict, Author: Zenko, Micah', 'Title: Fosering Peace After Civil War, Author: Mattes, Michaela.', 'Title: Systemic Disconnects: Why Regional Organizations Fail to Use Early Warning and Response Mechanisms, Author: Debiel, Thomas.', 'Title: Systemic Disconnects: Why Regional Organizations Fail to Use Early Warning and Response Mechanisms, Author: Debiel, Thomas.', 'Title: Cluster-Based Early Warning Indicators for Political Change in the Contemporary Levant, Author: Gerner, Deborah', 'Title: Early Warning and The Field: A Cargo Cult Science?, Author: Alexander, Austin', 'Title: Anticipating the Good, the Bad, and the Ugly, Author: O\'Brien, Sean.', 'Title: The politics of official apologies, Author: Nobles, M', 'Title: The guilt of nations, Author: Barkan, E.', 'Title: Gender, Status, and Leadership, Author: Ridgeway, Cecilia.', 'Title: Openness to experience, Author: McCrae, R. R', 'Title: Interpersonal conflict, agreeableness, and personality development, Author: Jensen-Campbell, L. A.', 'Title: Political Inclusion and the Dynamics of Democratization, Author: Dryzek, John.', 'Title: Evaluating Public Discourse in Newspaper Opinion Articles: Values-Framing and Integrative Complexity in Substance and Health Policy Issues, Author: Hoffman, Lindsey.', 'Title: Identity Versus Peace: Identity Wins, Author: Bekerman, Zvi.', 'Title: Returning the Gift -Utu in Intergroup Relations, Author: Metge, Joan.', 'Title: Openness to experience, Author: McCrae, R. R', 'Title: The relationship between openness to experience and political ideology, Author: van Hiel, A', 'Title: Prejudice and openness to the other: Investigating responses to testimonies of race-based suffering, Author: Cargile, A. C.', 'Title: Prejudie and openness to the other: Investigating responses to testimonies of race-based suffering, Author: Cargile, A. C', 'Title: Multicultural experiences reduce prejudice through personality shifts in openness to experience, Author: Sparkman, D. J.', 'Title: Creating and reducing intergroup conflict: The role of perspective-taking in affecting out-group evaluations, Author: Galinsky, A. D', 'Title: If we become friends, maybe I can change my perspective: Intergroup contact, endorsement of conflict narratives, and peace-related attitudes in Turkey, Author: Ulug, O. M.', 'Title: Similarity and nurturance: Two possible sources of empathy for strangers, Author: Batson, C. D', 'Title: Roots of empathy: Changing the world child by child, Author: Gordon, M', 'Title: The role of parents\' intergroup contact in fostering the well-being of adoptees: The extended intragroup effect, Author: Ferrari, L.', 'Title: Relative Deprivation Theory: An Overview and Conceptual Critique, Author: Walker, Iain.', 'Title: Gender and interpersonal violence, Author: Kruttschnitt, C', 'Title: Women\'s involvement in serious interpersonal violence, Author: Kruttschnitt, C', 'Title: Is femininity inherently peaceful? The construction of femininity in war, Author: Skjelsbaek, I.', 'Title: Out-group trust and conflict understandings:The perspective of Turks and Kurds in Turkey, Author: Celebi, E', 'Title: Peace vision and its socio-emotional antecedents: The role of forgiveness, trust, and inclusive victim perceptions, Author: Noor, M.', 'Title: Scientific Cooperation as an Instrument of U.S. Foreign Policy, 1938–1950, Author: Miller.', 'Title: Fosering Peace After Civil War, Author: Mattes, Michaela', 'Title: The idiosyncratic language of Israeli ‘peace’: A Cultural Approach to Critical Discourse Analysis, Author: Gavriely-Nury, Dalia.', 'Title: Fostering Peace After Civil War, Author: Mattes, Michaela', 'Title: The dark duo of post-colonial ideology: A model of symbolic exclusion and historical negation, Author: Sibley, C. G', 'Title: How the past weighs on the present: Social representations of history and their role in identity politics, Author: Liu, J. H', 'Title: Culture, social representations, and peacemaking: A symbolic theory of history and identity, Author: Liu, J. H', 'Title: Measuring the impacts of truth and reconciliation commissions: Placing the global \'success\' of TRCs in local perspective, Author: Ben-Josef Hirsch, M', 'Title: The Rule of Law and Transitional Justice in Conflict and Post-Conflict Societies, Author: United Nations Security CouncilTitle: A Conceptual Framework for Dealing with the Past – New Edition, Author: Baumgartner, E', 'Title: From transitional justice to dealing with the past: The role of norms in international peace mediation, Author: Pring, J.', 'Title: Transitional justice and peace building: Diagnosing and addressing the socioeconomic roots of violence through a human rights framework, Author: Laplante, L. S', 'Title: The politics of official apologies, Author: Nobles, M', 'Title: The guilt of nations, Author: Barkan, E', 'Title: Measuring the impacts of truth and reconciliation commissions: Placing the global \'success\' of TRCs in local perspective, Author: Ben-Josef Hirsch, M', 'Title: The Rule of Law and Transitional Justice in Conflict and PostConflict Societies, Author: United Nations Security CouncilTitle: From transitional justice to dealing with the past: The role of norms in international peace mediation, Author: Pring, J.', 'Title: Cooperation, competition, and conflict, Author: Deutsch, Morton', 'Title: New developments in social interdependence theory, Author: Johnson, David W', 'Title: Intergroup Cooperation, Author: Dovidio, John F', 'Title: The robbers cave experiment, Author: Sherif, M', 'Title: Cooperation, competition and goal interdependence in work teams: A multilevel approach, Author: Aritzeta, A', 'Title: A Quantitative Literature Review of Cooperative Learning Effects on High School and College Chemistry Achievement, Author: Bowen, C. W', 'Title: The relative effects of positive interdependence and group processing on student achievement and attitude in online cooperative learning, Author: Nam, C. W', 'Title: Effects of cooperative, competitive, and individualistic goal structures on achievement: A meta-analysis, Author: Johnson, D. W.', 'Title: Reaching across the dividing line: Building a collective vision for peace in Cyprus, Author: Broome, B.', 'Title: International environmental cooperation under fairness and reciprocity, Author: Hadjiyiannis, C', 'Title: PEACE AND SUSTAINABLE DEVELOPMENT WILL RISE OR FALL TOGETHER, Author: Krieger, D', 'Title: International Cooperation for Sustainable Development and Peace, Author: Westing, A', 'Title: Oil exploitation and human rights violations in Nigeria\'s oil producing communities, Author: Oluduro, O', 'Title: Oil exploration and ecological damage: The compensation policy in Nigeria, Author: Oluduro, O', 'Title: The role of civil society in addressing transboundary water issues in the Israeli-Palestinian context, Author: Aburdeineh, I.  ', 'Title: The Quality of Democracy: Why the Rule of Law Matters, Author: O\'Donnell, Guillermo.', 'Title: Modernization and Corruption, Author: Huntington, Samuel.', 'Title: The Role of the News Media in Peace Negotiations, Author: Wolfsfeld, Gadi.', 'Title: War and Misperception, Author: Jervis, Robert.''Title: Rally effects, threat, and attitude change: An integrative approach to understanding the role of emotion, Author: Lambert, A. J.''Title: Destined to die but not to wage war: How existential threat can contribute to escalation or de-escalation of violent intergroup conflict, Author: Jonas, E.', 'Title: Oil exploitation and human rights violations in Nigeria\'s oil producing communities, Author: Oluduro, O', 'Title: Oil exploration and ecological damage: The compensation policy in Nigeria, Author: Oluduro, O', 'Title: Sustainable development and human rights: An integrative conception, Author: McGoldrick, D', 'Title: Inclusive sustainable development: A human rights perspective, Author: Arts, K', 'Title: Transforming Our World: The 2030 Agenda for Sustainable Development, Author: UN General AssemblyTitle: The Philippines and the United Nations: 60 years of partnership for world peace, sustainable development and respect for human rights, Author: Foreign Services Institute (Philippines)Title: Traps of violence: A human rights analysis of the relationship between peace and sustainable development, Author: Andreassen, B. A.', 'Title: Inclusive sustainable development: A human rights perspective, Author: Arts, K', 'Title: The effect of intergroup comparison on willingness to perform sustainable behavior, Author: Ferguson, M. A', 'Title: Transforming Our World: The 2030 Agenda for Sustainable Development, Author: UN General Assembly', 'Title: Learning communities, cities and regions for sustainable development and global citizenship, Author: Morgan, A. D', 'Title: Global citizenship: Abstraction or framework for action?, Author: Davies, L', 'Title: A curriculum for global citizenship, Author: Oxfam.', 'Title: Contextual effects on prejudiced attitudes: When the presence of others leads to more egalitarian responses, Author: Castelli, L', 'Title: Aversive racism and selection decisions: 1989 and 1999, Author: Dovidio, J. F', 'Title: Beliefs about inequality: America’s view of what is and what ought to be, Author: Kluegel, J.R', 'Title: Social norms and the expression and suppression of prejudice: The struggle for internalization, Author: Crandall, C.S.', 'Title: Direct and indirect intergroup friendship effects: Testing the moderating role of the affective-cognitive bases of prejudice, Author: Paolini, S', 'Title: Building trust in a postconflict society: An integrative model of cross-group friendship and intergroup emotions, Author: Kenworthy, J. B', 'Title: Promoting intergroup trust among adolescents and young adults, Author: Turner, R. N', 'Title: The resolution of conflict: Constructive and destructive processes, Author: Deutsch, M', 'Title: Peace vision and its socio-emotional antecedents: The role of forgiveness, trust, and inclusive victim perceptions, Author: Noor, M', 'Title: It takes two to tango: An interdependence analysis of the spiraling of perceived trustworthiness and cooperation in interpersonal and intergroup relationships, Author: Ferrin, D. L', 'Title: Intergroup trust and reciprocity in strategic interactions: Effects of group decision-making mechanisms, Author: Song, F', 'Title: Getting to know you: Reputation and trust in a two-person economic exchange, Author: King-Casas, B.  ', 'Title: Imagining intergroup contact enables member-to-group generalization, Author: Stathi, S', 'Title: Out-group trust, intergroup anxiety, and out-group attitude as mediators of the effect of imagined intergroup contact on intergroup behavioral tendencies, Author: Turner, R. N', 'Title: Hope in the Middle East: Malleability beliefs, hope, and the willingness to compromise for peace, Author: Cohen-Chen, S', 'Title: The psychological study of positive behavior across group boundaries: An overview, Author: Siem, B.', 'Title: Psychological dynamics of insight: Relevance to international negotiation, Author: Sargent, N', 'Title: What have they done for us lately? The dynamics of reciprocity in intergroup contexts, Author: Doosje, B', 'Title: The fleeting gleam of praise: Cognitive processes underlying behavioral reactions to self-relevant feedback, Author: Swann, W. B', 'Title: When does introspection bear fruit? Self-reflection, self-insight, and interpersonal choices, Author: Hixon, J. G', 'Title: Selective interaction as a strategy for identity maintenance: An affect control model, Author: Robinson, D. T', 'Title: Agreeable fancy or disagreeable truth? Reconciling self-enhancement and self-verification, Author: Swann, W. B., Jr', 'Title: Allure of negative feedback: Self-verification strivings among depressed persons, Author: Swann, W. B', 'Title: Depression and the search for negative evaluations: More evidence of the role of self-verification strivings, Author: Swann, W. B', 'Title: Why threats trigger compensatory reactions: The need for coherence and quest for self-verification, Author: Swann, W. B., Jr', 'Title: The distinctive effects of empathy and hope in intractable conflicts, Author: Rosler, N', 'Title: The resolution of conflict: Constructive and destructive processes, Author: Deutsch, M', 'Title: Universals in the content and structure of values: Theoretical advances and empirical tests in 20 countries, Author: Schwartz, S. H', 'Title: Culture of peace, Author: Fry, D. P', 'Title: Stereotypes and prejudice: Their automatic and controlled components, Author: Devine, P. G', 'Title: The Influence of Personality on Conflict Resolution Styles and Choices, Author: Sandy, S. V', 'Title: Does truth lead to reconciliation? Testing the causal assumptions of the South African truth and reconciliation process, Author: Gibson, J. L', 'Title: The social psychology of intergroup relations: Social categorization, ingroup bias, and outgroup prejudice, Author: Brewer, M. B', 'Title: The neuroscience of intergroup relations: An integrative review, Author: Cikara, M.', 'Title: The impacts of the sustainable communities initiative regional planning grants on planning and equity in three metropolitan regions, Author: Arias, J. S.', 'Title: Cooperation, competition, and conflict, Author: Deutsch, M', 'Title: Intergroup threat and outgroup attitudes: A meta-analytic review, Author: Riek, B. M', 'Title: Political intolerance in the context of democratic theory, Author: Gibson, J. L', 'Title: Intergroup reconciliation: Effects of adversary\'s expressions of empathy, responsibility, and recipients\' trust, Author: Nadler, A', 'Title: Changing brains, changing perspectives: The neurocognitive development of reciprocity, Author: van den Bos, W', 'Title: The spiral of distrust: (Non‐) cooperation in a repeated trust game is predicted by anger and individual differences in negative reciprocity orientation, Author: Harth, N. S', 'Title: Expectations among Aboriginal peoples in Canada regarding the potential impacts of a government apology, Author: Bombay, A', 'Title: The transmission of trauma across generations: identification with parental trauma in children of Holocaust survivors, Author: Rowland-Kelin, D', 'Title: Individual-level evidence for the causes and consequences of social capital, Author: Brehm, J', 'Title: The rise and fall of political engagement among Latinos: The role of identity and perceptions of discrimination, Author: Schildkraut, D. J', 'Title: The hand-in-hand spread of mistrust and misinformation in Flint: the water crisis not only left infrastructure and government agencies in need of cleaning up; the information landscape was also messy, Author: Roy, S', 'Title: Beyond distrust: Getting even and the need for revenge, Author: Bies, R. J', 'Title: The pivotal points in planning: How the use of contracts influence trust dynamics and vice versa, Author: de Ries, J. R.', 'Title: The nuclear taboo: The United Sates and the non-use of nuclear weapons since 1945, Author: Tannenwald, N.', 'Title: The impact of intergroup emotions on forgiveness in Northern Ireland, Author: Tam, T', 'Title: Why does fear override hope in societies engulfed by intractable conflict, as it does in the Israeli society?, Author: Bar‐Tal, D', 'Title: Forgive and forget? Antecedents and consequences of intergroup forgiveness in Bosnia and Herzegovina, Author: Cehajic, S.', 'Title: Political conservatism, need for cognitive closure, and intergroup hostility, Author: De Zavala, A. G', 'Title: Groups as epistemic providers: Need for closure and the unfolding of group-centrism, Author: Kruglanski, A. W', 'Title: Membership has its (epistemic) rewards: Need for closure effects on in-group bias, Author: Shah, J. Y.', 'Title: Attachment theory and concern for others\' welfare: Evidence that activation of the sense of secure base promotes endorsement of self-transcendence values, Author: Mikulincer, M.', 'Title: EDUCATION AND POLITICAL TOLERANCE: TESTING THE EFFECTS OF COGNITIVE SOPHISTICATION AND TARGET GROUP AFFECT, Author: Bobo, Lawrence.', 'Title: The distinctive effects of empathy and hope in intractable conflicts, Author: Rosler, N', 'Title: Hope in the Middle East: Malleability beliefs, hope, and the willingness to compromise for peace, Author: Cohen-Chen, S', 'Title: Beliefs predicting peace, beliefs predicting war: Jewish Americans and the Israeli-Palestinian conflict, Author: Hagai, E. B.', 'Title: Prejudice, polyculturalism, and the influence of contact and moral exclusion: A comparison of responses toward LGBI, TI, and refugee groups, Author: Healy, E', 'Title: Empathy and humanitarianism predict preferential moral responsiveness to in-group and out-groups, Author: Redford, L', 'Title: To accept or not to accept: Level of moral concern impacts on tolerance of Muslim minority practices, Author: Hirsch, M.', 'Title: Effects of child abuse, adolescent violence, peer approval and pro‐violence attitudes on intimate partner violence in adulthood, Author: Herrenkohl, T. I', 'Title: Humiliation and the inertia effect: implications for understanding violence and compromise in intractable intergroup conflicts, Author: Ginges, J.', 'Title: Cultural Intelligence and Global Identity in Multicultural Teams, Author: Shokef, Efret', 'Title: Intergroup violence and intergroup attributions, Author: Hunter, J. A.', 'Title: Fear as a correlate of authoritarianism, Author: Eigenberger, M. E', 'Title: Threat as a factor in authoritarianism: An analysis of archival data, Author: Sales, S. M', 'Title: Developmental Antecedents of Political Ideology: A Longitudinal Investigation From Birth to Age 18 Years, Author: Fraley', 'Title: Intergroup beliefs: Investigations from the social side, Author: Stagnor, C', 'Title: The irony of harmony: Intergroup contact can produce false expectations for equality, Author: Saguy, T.', 'Title: Value priorities and behavior: Applying, Author: Schwartz, S', 'Title: Value priorities and readiness for out-group social contact, Author: Sagiv, L', 'Title: Attitudes of physical distance to an individual with schizophrenia: The moderating effect of self-transcendent values, Author: Norman, R. M. G.', 'Title: The limited prosocial effects of meditation: A systematic review and meta-analysis, Author: Kreplin, U.''Title: Towards a theoretical model of personal peacefulness, Author: Sims, G. K.', 'Title: Literacy instruction: Technology and technique, Author: de Castell, S.', 'Title: Influence of social motives on integrative negotiation: a meta-analytic review and test of two theories, Author: De Dreu, C. K', 'Title: Cooperative Orientation, Trust, and Reciprocity, Author: Meeker, Barbara.', 'Title: The apple does not fall far from the tree, or does it? A meta-analysis of parent–child similarity in intergroup attitudes, Author: Degner, J', 'Title: A integrative theory of intergroup conflict, Author: Tajfel, H', 'Title: The authoritarian personality, Author: Adorno, T. W', 'Title: Wither political socialization research, Author: Sears, D. O', 'Title: Intergenerational transmission and the formation of cultural orientations in adolescence and young adulthood, Author: Vollebergh, W. A. M', 'Title: Childhood punishment, denial, and political attitudes, Author: Milburn, M. A', 'Title: The other ‘‘authoritarian personality’’, Author: Altemeyer, B', 'Title: In search of the antecedents of adolescent authoritarianism: The relative contribution of parental goal promotion and parenting style promotion, Author: Duriez, B.', 'Title: Examining the possibilities of school transformation for peace in northern Ireland from a narrative perspective, Author: Smith, R', 'Title: The role of language in peacebuilding: The case of the 2008 Kenyan Coalition Government, Author: Barasa, M. S', 'Title: Finding common ground: Learning the language of peace, Author: Bleeker, G. W', 'Title: Speaking the language of peace: Chamoru resistance and rhetoric in Guahan\'s self-determination movement, Author: Na\'puti, T. R', 'Title: Antecedents and consequences of social identity complexity: Intergroup contact, distinctiveness threat, and outgroup attitudes, Author: Schmid, K', 'Title: Social identity complexity, Author: Roccas, S', 'Title: Social identity complexity: Its correlates and antecedents, Author: Miller, K. P.', 'Title: The power of non-violence, Author: Gregg, R. B', 'Title: Intimate partner physical abuse perpetration and victimization risk factors: A meta-analytic review, Author: Stith, S. M', 'Title: Does changing behavioral intentions engender behavior change? A meta-analysis of the experimental evidence, Author: Webb, T. L', 'Title: Reconciliation sentiment among victims of genocide in Rwanda: Conceptualizations, and relationships with mental health, Author: Mukashema, I', 'Title: The power of integral nonviolence: On the significance of Gandhi today, Author: Tully, J.', 'Title: Official or political apologies and improvement of intergroup relations: A neo-Durkheimian approach to official apologies as rituals, Author: Páez, Darío.', 'Title: Why Egalitarianism Might Be Good for Your Health: Physiological Thriving During Stressful Intergroup Encounters, Author: Mendes, Wendy Berry.']
for str in strings:
    doi = find_doi(str)
    if doi:
        dois.append(doi)
print(dois)


