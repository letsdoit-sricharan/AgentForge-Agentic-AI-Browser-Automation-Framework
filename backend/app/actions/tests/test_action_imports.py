"""
Tests the public Action Library API.
"""

from app.actions import (
    BackAction,
    ForwardAction,
    NavigateAction,
    RefreshAction,
    WaitAction,
    ClickAction,
    DoubleClickAction,
    RightClickAction,
    HoverAction,
    FillAction,
    ClearAction,
    CheckAction,
    UncheckAction,
    SelectOptionAction,
    FocusAction,
    BlurAction,
)


def test_imports():

    print("\n==============================")
    print(" Action Library Import Test ")
    print("==============================\n")

    actions = [
        BackAction,
        ForwardAction,
        NavigateAction,
        RefreshAction,
        WaitAction,
        ClickAction,
        DoubleClickAction,
        RightClickAction,
        HoverAction,
        FillAction,
        ClearAction,
        CheckAction,
        UncheckAction,
        SelectOptionAction,
        FocusAction,
        BlurAction,
    ]

    for action in actions:
        print(f"✓ {action.__name__}")

    print("\n✅ All Action Library imports are valid.")


if __name__ == "__main__":
    test_imports()