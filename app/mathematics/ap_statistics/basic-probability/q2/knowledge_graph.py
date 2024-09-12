import json
from parameters import *


class Node:
    def __init__(self, concept_id, concept_uuid, concept_question, concept, similar_concepts, concept_formula, calc_required,
                 concept_rephrases):
        self.concept_id = concept_id
        self.concept_uuid = concept_uuid
        self.concept_question = concept_question
        self.concept = concept
        self.similar_concepts = similar_concepts
        self.concept_rephrases = concept_rephrases
        if concept_formula == "":
            self.concept_formula = None
        else:
            self.concept_formula = concept_formula
        self.calc_required = calc_required

    def __eq__(self, other):
        if self.concept_uuid in other.similar_concepts:
            return True
        if other.concept_uuid in self.similar_concepts:
            return True
        return False


class Edge:
    def __init__(self, startNode_id, endNode_id):
        if startNode_id == endNode_id:
            print("Edge cannot have same start and end nodes")
        else:
            self.startNode = startNode_id
            self.endNode = endNode_id

    def __eq__(self, other):
        if self.startNode == other.startNode and self.endNode == other.endNode:
            return True
        return False

    def __hash__(self):
        return hash((self.startNode, self.endNode))


class Graph():
    def __init__(self, client=None):
        self.openaiClient = client
        self.nodesDict = {}
        self.adjacencyDict = {}
        self.nodeParents = {}

    def add_node(self, concept_id, concept_uuid, concept_question, concept, similar_concepts, concept_formula, calc_required,
                 concept_rephrases=""):
        node = Node(concept_id, concept_uuid, concept_question, concept,
                    similar_concepts, concept_formula, calc_required, concept_rephrases)
        # Add node to nodes dictionary
        if concept_id not in self.nodesDict:
            self.nodesDict[concept_id] = node

    def add_edge(self, concept_id1, concept_id2):
        edge = Edge(concept_id1, concept_id2)

        # Add to adjacency dictionary
        if edge.startNode in self.adjacencyDict:
            self.adjacencyDict[edge.startNode].add(edge.endNode)
        else:
            self.adjacencyDict[edge.startNode] = {edge.endNode}

        # Add to nodesParent dictionary
        if edge.endNode in self.nodeParents:
            self.nodeParents[edge.endNode].add(edge.startNode)
        else:
            self.nodeParents[edge.endNode] = {edge.startNode}

    def populate_graph_from_JSON(self, filename):
        f = open(filename)
        json_obj = json.load(f)
        uuid_dict = {}
        for concept in json_obj["concepts"]:
            uuid_dict[concept["concept_uuid"]] = concept["concept_id"]
        for concept in json_obj["concepts"]:
            if "concept_rephrases" in concept:
                self.add_node(concept["concept_id"], concept["concept_uuid"], concept["concept_question"], concept["concept"],
                              set(concept["similar_concepts"]
                                  ), concept["concept_formula"], concept["calculation_required"],
                              concept_rephrases=concept["concept_rephrases"])
            else:
                self.add_node(concept["concept_id"], concept["concept_uuid"], concept["concept_question"], concept["concept"],
                              set(concept["similar_concepts"]), concept["concept_formula"], concept["calculation_required"])
            for parent_concept_uuid in concept["parent_concepts"]:
                self.add_edge(
                    uuid_dict[parent_concept_uuid], concept["concept_id"])

    def addNodeFromKG(self, KG, node_id):
        stack = [node_id]
        while stack:
            nextNode = stack.pop(0)
            if nextNode not in self.nodesDict:
                self.nodesDict[nextNode] = KG.nodesDict[nextNode]
            if nextNode in KG.nodeParents:
                for parent_node in KG.nodeParents[nextNode]:
                    stack.append(parent_node)
                    edge = Edge(parent_node, nextNode)
                    # Add to adjacency dictionary
                    if edge.startNode in self.adjacencyDict:
                        self.adjacencyDict[edge.startNode].add(edge.endNode)
                    else:
                        self.adjacencyDict[edge.startNode] = {edge.endNode}
                    # Add to nodesParent dictionary
                    if edge.endNode in self.nodeParents:
                        self.nodeParents[edge.endNode].add(edge.startNode)
                    else:
                        self.nodeParents[edge.endNode] = {edge.startNode}

    def populate_graph_from_adjacency_dict(self, adjacency_dict, KG):
        self.adjacencyDict = adjacency_dict
        for parent_node in adjacency_dict:
            if parent_node not in self.nodesDict:
                self.nodesDict[parent_node] = KG.nodesDict[parent_node]
            for child_node in adjacency_dict[parent_node]:
                if child_node not in self.nodesDict:
                    self.nodesDict[child_node] = KG.nodesDict[child_node]
                if child_node in self.nodeParents:
                    self.nodeParents[child_node].add(parent_node)
                else:
                    self.nodeParents[child_node] = {parent_node}

    def remove_nodes(self, nodes):
        for node_id in nodes:
            del self.nodesDict[node_id]
            if node_id in self.adjacencyDict:
                del self.adjacencyDict[node_id]
            if node_id in self.nodeParents:
                del self.nodeParents[node_id]
            for id in self.adjacencyDict:
                if node_id in self.adjacencyDict[id]:
                    self.adjacencyDict[id].remove(node_id)
            for id in self.nodeParents:
                if node_id in self.nodeParents[id]:
                    self.nodeParents[id].remove(node_id)

    # A subgraph is said to be valid if all its nodes have parent nodes as part of the subgraph.
    def get_valid_subgraph(self, nodes, start_nodes):
        valid_subgraph = []
        for start_node in start_nodes:
            if start_node not in nodes:
                return valid_subgraph, nodes
        nodesVisited = set()
        stack = []
        nodes_left = nodes.copy()
        for id in start_nodes:
            stack.append(id)
        while stack:
            nextConceptID = stack.pop(0)
            if nextConceptID in nodes_left:
                valid_subgraph.append(nextConceptID)
                nodes_left.remove(nextConceptID)
                if nextConceptID in self.adjacencyDict:
                    for node in self.adjacencyDict[nextConceptID]:
                        if node not in nodesVisited:
                            if len(self.nodeParents[node]) == 1:
                                stack.append(node)
                                nodesVisited.add(node)
                            else:
                                remainingParents = self.nodeParents[node] - {
                                    nextConceptID}
                                all_parents_present = True
                                for parent_node in remainingParents:
                                    if parent_node not in valid_subgraph:
                                        all_parents_present = False
                                        break
                                if all_parents_present:
                                    stack.append(node)
                                    nodesVisited.add(node)
        return valid_subgraph, nodes_left

    def get_missing_concepts(self, nodes, start_nodes):
        nodesVisited = set()
        stack = []
        for id in start_nodes:
            stack.append(id)
        missing_nodes = []
        nodesLeft = nodes.copy()
        while stack:
            nextConceptID = stack.pop(0)
            if nextConceptID in nodes:
                nodesLeft.remove(nextConceptID)
                if not nodesLeft:
                    break
            else:
                similar_node_present = False
                for similar_concept in self.nodesDict[nextConceptID].similar_concepts:
                    if similar_concept in nodes:
                        similar_node_present = True
                if not similar_node_present:
                    missing_nodes.append(nextConceptID)
            if nextConceptID in self.adjacencyDict:
                for node in self.adjacencyDict[nextConceptID]:
                    if node not in nodesVisited:
                        stack.append(node)
                        nodesVisited.add(node)
        return missing_nodes

    def get_missing_parent_concepts(self, nodes, start_nodes):
        nodesVisited = set()
        stack = []
        for id in start_nodes:
            stack.append(id)
        missing_nodes = []
        while stack:
            nextConceptID = stack.pop(0)
            if nextConceptID in nodes:
                break
            else:
                missing_nodes.append(nextConceptID)
            if nextConceptID in self.adjacencyDict:
                for node in self.adjacencyDict[nextConceptID]:
                    if node not in nodesVisited:
                        stack.append(node)
                        nodesVisited.add(node)
        return missing_nodes

    def get_concept_questions(self, concept_ids):
        id_to_ind = {}
        concept_questions_dict = {}
        ind = 1
        for concept_id in concept_ids:
            similar_id_present = False
            for id in id_to_ind:
                if self.nodesDict[concept_id] == self.nodesDict[id]:
                    similar_id_present = True
                    similar_id = id
                    break
            if similar_id_present:
                id_to_ind[concept_id] = id_to_ind[similar_id]
            else:
                id_to_ind[concept_id] = ind
                ind = ind + 1
        for concept_id in id_to_ind:
            if id_to_ind[concept_id] in concept_questions_dict:
                concept_questions_dict[id_to_ind[concept_id]] = concept_questions_dict[id_to_ind[concept_id]] + " OR " \
                    + self.nodesDict[concept_id].concept_question
            else:
                concept_questions_dict[id_to_ind[concept_id]
                                       ] = self.nodesDict[concept_id].concept_question
        missing_questions_string = ""
        for question_num in concept_questions_dict:
            missing_questions_string = missing_questions_string + \
                str(question_num) + ") " + \
                concept_questions_dict[question_num] + "\n"
        return missing_questions_string, id_to_ind
