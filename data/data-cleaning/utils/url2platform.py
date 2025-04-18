from utils.enums import TutorialPlatform
from utils.enums import ProblemPlatform


def is_problem_url(url: str) -> bool:
    if problem_url2platform(url) == ProblemPlatform.UNKNOWN:
        return False
    return True


def problem_url2platform(url: str) -> ProblemPlatform:
    if "leetcode.com/problems" in url:
        return ProblemPlatform.LEETCODE
    elif "neetcode.io/problems" in url:
        return ProblemPlatform.NEETCODE
    elif "geeksforgeeks.org/problems" in url:
        return ProblemPlatform.GFG
    elif "naukri.com/code360/problems" in url:
        return ProblemPlatform.CODE360
    elif "interviewbit.com/problems" in url:
        return ProblemPlatform.INTERVIEWBIT
    elif "codechef.com/problems" in url:
        return ProblemPlatform.CODECHEF
    elif "codeforces.com" in url:
        return ProblemPlatform.CODEFORCES
    elif "atcoder.jp" in url:
        return ProblemPlatform.ATCODER
    elif "topcoder.com" in url:
        return ProblemPlatform.TOPCODER
    elif "cses.fi" in url:
        return ProblemPlatform.CSES
    elif "lintcode.com/problem" in url:
        return ProblemPlatform.LINTCODE
    elif "spoj.com/problems" in url:
        return ProblemPlatform.SPOJ
    elif "hackerearth.com/problem" in url or "hackerearth.com/practice" in url:
        return ProblemPlatform.HACKEREARTH
    elif "hackerrank.com/challenges" in url:
        return ProblemPlatform.HACKERRANK
    else:
        return ProblemPlatform.UNKNOWN
    

def tutorial_url2platform(url: str) -> TutorialPlatform:
    """
    Supports GeeksForGeeks, Programiz, Scaler, Code 360, YouTube
    """
    if "geeksforgeeks.org" in url:
        return TutorialPlatform.GFG
    elif "programiz" in url:
        return TutorialPlatform.PROGRAMIZ
    elif "scaler" in url:
        return TutorialPlatform.SCALER
    elif "naukri.com/code360" in url:
        return TutorialPlatform.CODE360
    elif "youtube.com" in url:
        return TutorialPlatform.YOUTUBE
    else:
        print(f"Unknown platform for tutorial url: {url}")
    return TutorialPlatform.UNKNOWN
    