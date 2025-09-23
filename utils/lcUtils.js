import { LeetCode } from "leetcode-query";

async function slug2details(slug) {
  const leetcode = new LeetCode();
  const problem = await leetcode.problem(slug);
  return { questionId: problem.questionId, title: problem.title };
}