# main.py

from spoon_game import SpoonGame

def main():
    game = SpoonGame()

    while not game.state.game_finished:
        print(game.get_status())
        action = input("按[回车]尝试掰弯勺子(输入q退出): ")
        if action.lower() == 'q':
            break
        result = game.try_bend_spoon()
        print(result)

    print("游戏进度已自动保存。")
    if game.state.game_finished:
        print("你已完成整个游戏！")

if __name__ == "__main__":
    main()