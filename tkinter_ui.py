import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import filedialog
from utils.config import resource_path, load_external_config
from main import UpdateSource
import os
import asyncio
import threading
import webbrowser

config_path = resource_path("user_config.py")
default_config_path = resource_path("config.py")
config = (
    load_external_config("user_config.py")
    if os.path.exists(config_path)
    else load_external_config("config.py")
)


class TkinterUI:

    def __init__(self, root):
        self.root = root
        self.root.title("直播源接口更新工具")
        self.version = "v1.3.3"
        self.update_source = UpdateSource()
        self.update_running = False
        self.config_entrys = [
            "open_update_checkbutton",
            "open_driver_checkbutton",
            "open_proxy_checkbutton",
            "source_file_entry",
            "source_file_button",
            "final_file_entry",
            "final_file_button",
            "open_subscribe_checkbutton",
            "open_multicast_checkbutton",
            "open_online_search_checkbutton",
            "open_sort_checkbutton",
            "favorite_list_text",
            "favorite_page_num_entry",
            "default_page_num_entry",
            "urls_limit_entry",
            "response_time_weight_entry",
            "resolution_weight_entry",
            "ipv_type_combo",
            "recent_days_entry",
            "domain_blacklist_text",
            "url_keywords_blacklist_text",
            "subscribe_urls_text",
            "region_list_text",
        ]
        self.result_url = None

    def format_list(self, text):
        return [f"{item.strip()}" for item in text.split(",") if item.strip()]

    def update_open_update(self):
        config.open_update = self.open_update_var.get()

    def select_source_file(self):
        filepath = filedialog.askopenfilename(
            initialdir=os.getcwd(), title="选择模板文件", filetypes=[("txt", "*.txt")]
        )
        if filepath:
            self.source_file_entry.delete(0, tk.END)
            self.source_file_entry.insert(0, filepath)
            config.source_file = filepath

    def select_final_file(self):
        filepath = filedialog.askopenfilename(
            initialdir=os.getcwd(), title="选择结果文件", filetypes=[("txt", "*.txt")]
        )
        if filepath:
            self.final_file_entry.delete(0, tk.END)
            self.final_file_entry.insert(0, filepath)
            config.final_file = filepath

    def update_open_subscribe(self):
        config.open_subscribe = self.open_subscribe_var.get()

    def update_open_multicast(self):
        config.open_multicast = self.open_multicast_var.get()

    def update_open_online_search(self):
        config.open_online_search = self.open_online_search_var.get()

    def update_open_driver(self):
        config.open_driver = self.open_driver_var.get()

    def update_open_proxy(self):
        config.open_proxy = self.open_proxy_var.get()

    def update_open_sort(self):
        config.open_sort = self.open_sort_var.get()

    def update_favorite_list(self, event):
        config.favorite_list = self.format_list(
            self.favorite_list_text.get(1.0, tk.END)
        )

    def update_favorite_page_num(self, event):
        config.favorite_page_num = self.favorite_page_num_entry.get()

    def update_default_page_num(self, event):
        config.default_page_num = self.default_page_num_entry.get()

    def update_urls_limit(self, event):
        config.urls_limit = self.urls_limit_entry.get()

    def update_response_time_weight(self, event):
        config.response_time_weight = self.response_time_weight_entry.get()

    def update_resolution_weight(self, event):
        config.resolution_weight = self.resolution_weight_entry.get()

    def update_ipv_type(self, event):
        config.ipv_type = f'"{self.ipv_type_combo.get()}"'

    def update_recent_days(self, event):
        config.recent_days = self.recent_days_entry.get()

    def update_url_keywords_blacklist(self, event):
        config.url_keywords_blacklist = self.format_list(
            self.url_keywords_blacklist_text.get(1.0, tk.END)
        )

    def update_domain_blacklist(self, event):
        config.domain_blacklist = self.format_list(
            self.domain_blacklist_text.get(1.0, tk.END)
        )

    def update_url_keywords_blacklist(self, event):
        config.url_keywords_blacklist = self.format_list(
            self.url_keywords_blacklist_text.get(1.0, tk.END)
        )

    def update_subscribe_urls(self, event):
        config.subscribe_urls = self.format_list(
            self.subscribe_urls_text.get(1.0, tk.END)
        )

    def update_region_list(self, event):
        config.region_list = self.format_list(self.region_list_text.get(1.0, tk.END))

    def view_result_link_callback(self, event):
        webbrowser.open_new_tab(self.result_url)

    def save_config(self):
        config_values = {
            "open_update": self.open_update_var.get(),
            "source_file": f'"{self.source_file_entry.get()}"',
            "final_file": f'"{self.final_file_entry.get()}"',
            "favorite_list": self.format_list(self.favorite_list_text.get(1.0, tk.END)),
            "open_online_search": self.open_online_search_var.get(),
            "favorite_page_num": self.favorite_page_num_entry.get(),
            "default_page_num": self.default_page_num_entry.get(),
            "urls_limit": self.urls_limit_entry.get(),
            "open_driver": self.open_driver_var.get(),
            "open_proxy": self.open_proxy_var.get(),
            "open_sort": self.open_sort_var.get(),
            "response_time_weight": self.response_time_weight_entry.get(),
            "resolution_weight": self.resolution_weight_entry.get(),
            "recent_days": self.recent_days_entry.get(),
            "ipv_type": f'"{self.ipv_type_combo.get()}"',
            "domain_blacklist": self.format_list(
                self.domain_blacklist_text.get(1.0, tk.END)
            ),
            "url_keywords_blacklist": self.format_list(
                self.url_keywords_blacklist_text.get(1.0, tk.END)
            ),
            "open_subscribe": self.open_subscribe_var.get(),
            "subscribe_urls": self.format_list(
                self.subscribe_urls_text.get(1.0, tk.END)
            ),
            "open_multicast": self.open_multicast_var.get(),
            "region_list": self.format_list(self.region_list_text.get(1.0, tk.END)),
        }

        for key, value in config_values.items():
            setattr(config, key, value)
        user_config_file = (
            "user_config.py" if os.path.exists("user_config.py") else "config.py"
        )
        with open(
            resource_path(user_config_file, persistent=True), "w", encoding="utf-8"
        ) as f:
            for key, value in config_values.items():
                f.write(f"{key} = {value}\n")
        messagebox.showinfo("提示", "保存成功")

    async def run_update(self):
        self.update_running = not self.update_running
        if self.update_running:
            self.run_button.config(text="取消更新", state="normal")
            for entry in self.config_entrys:
                getattr(self, entry).config(state="disabled")
            self.progress_bar["value"] = 0
            self.progress_label.pack()
            self.view_result_link.pack()
            self.progress_bar.pack()
            await self.update_source.start(self.update_progress)
        else:
            self.stop()
            self.update_source.stop()
            self.run_button.config(text="开始更新", state="normal")
            for entry in self.config_entrys:
                getattr(self, entry).config(state="normal")
            self.progress_bar.pack_forget()
            self.view_result_link.pack_forget()
            self.progress_label.pack_forget()

    def on_run_update(self):
        def run_loop():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.run_update())

        self.thread = threading.Thread(target=run_loop, daemon=True)
        self.thread.start()

    def stop(self):
        asyncio.get_event_loop().stop()

    def update_progress(self, title, progress, finished=False, url=None):
        self.progress_bar["value"] = progress
        progress_text = f"{title}, 进度: {progress}%" if not finished else f"{title}"
        self.progress_label["text"] = progress_text
        self.root.update()
        if finished:
            self.run_button.config(text="开始更新", state="normal")
            self.update_running = False
            for entry in self.config_entrys:
                getattr(self, entry).config(state="normal")
            if url:
                self.view_result_link.config(text=url)
                self.result_url = url

    def init_UI(self):

        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both", padx=10, pady=0)

        frame1 = ttk.Frame(notebook, width=500, height=500)
        frame2 = ttk.Frame(notebook, width=500, height=500)
        frame3 = ttk.Frame(notebook, width=500, height=500)
        frame4 = ttk.Frame(notebook, width=500, height=500)

        notebook.add(frame1, text="通用设置")
        notebook.add(frame2, text="在线搜索")
        notebook.add(frame3, text="订阅源")
        notebook.add(frame4, text="组播源")

        frame1_open_update = tk.Frame(frame1)
        frame1_open_update.pack(fill=tk.X)

        self.open_update_label = tk.Label(frame1_open_update, text="开启更新:", width=8)
        self.open_update_label.pack(side=tk.LEFT, padx=4, pady=8)
        self.open_update_var = tk.BooleanVar(value=config.open_update)
        self.open_update_checkbutton = ttk.Checkbutton(
            frame1_open_update,
            variable=self.open_update_var,
            onvalue=True,
            offvalue=False,
            command=self.update_open_update,
            text="(关闭则只运行结果页面服务)",
        )
        self.open_update_checkbutton.pack(side=tk.LEFT, padx=4, pady=8)

        frame1_source_file = tk.Frame(frame1)
        frame1_source_file.pack(fill=tk.X)

        self.source_file_label = tk.Label(frame1_source_file, text="模板文件:", width=8)
        self.source_file_entry = tk.Entry(frame1_source_file)
        self.source_file_label.pack(side=tk.LEFT, padx=4, pady=8)
        self.source_file_entry.pack(fill=tk.X, padx=4, expand=True)
        self.source_file_entry.insert(0, config.source_file)

        frame1_source_file_select = tk.Frame(frame1)
        frame1_source_file_select.pack(fill=tk.X)

        self.source_file_button = tk.Button(
            frame1_source_file_select, text="选择文件", command=self.select_source_file
        )
        self.source_file_button.pack(side=tk.LEFT, padx=4, pady=0)

        frame1_final_file = tk.Frame(frame1)
        frame1_final_file.pack(fill=tk.X)

        self.final_file_label = tk.Label(frame1_final_file, text="结果文件:", width=8)
        self.final_file_entry = tk.Entry(frame1_final_file)
        self.final_file_label.pack(side=tk.LEFT, padx=4, pady=8)
        self.final_file_entry.pack(fill=tk.X, padx=4, expand=True)
        self.final_file_entry.insert(0, config.final_file)

        frame1_final_file_select = tk.Frame(frame1)
        frame1_final_file_select.pack(fill=tk.X)

        self.final_file_button = tk.Button(
            frame1_final_file_select, text="选择文件", command=self.select_final_file
        )
        self.final_file_button.pack(side=tk.LEFT, padx=4, pady=0)

        frame1_mode = tk.Frame(frame1)
        frame1_mode.pack(fill=tk.X)
        frame1_mode_params_column1 = tk.Frame(frame1_mode)
        frame1_mode_params_column1.pack(side=tk.LEFT, fill=tk.Y)
        frame1_mode_params_column2 = tk.Frame(frame1_mode)
        frame1_mode_params_column2.pack(side=tk.RIGHT, fill=tk.Y)

        self.open_driver_label = tk.Label(
            frame1_mode_params_column1, text="浏览器模式:", width=12
        )
        self.open_driver_label.pack(side=tk.LEFT, padx=4, pady=8)
        self.open_driver_var = tk.BooleanVar(value=config.open_driver)
        self.open_driver_checkbutton = ttk.Checkbutton(
            frame1_mode_params_column1,
            variable=self.open_driver_var,
            onvalue=True,
            offvalue=False,
            command=self.update_open_driver,
            text="(较消耗性能)",
        )
        self.open_driver_checkbutton.pack(side=tk.LEFT, padx=4, pady=8)

        self.open_proxy_label = tk.Label(
            frame1_mode_params_column2, text="开启代理:", width=12
        )
        self.open_proxy_label.pack(side=tk.LEFT, padx=4, pady=8)
        self.open_proxy_var = tk.BooleanVar(value=config.open_proxy)
        self.open_proxy_checkbutton = ttk.Checkbutton(
            frame1_mode_params_column2,
            variable=self.open_proxy_var,
            onvalue=True,
            offvalue=False,
            command=self.update_open_proxy,
            text="(自动获取免费代理)",
        )
        self.open_proxy_checkbutton.pack(side=tk.LEFT, padx=4, pady=8)

        frame1_channel = tk.Frame(frame1)
        frame1_channel.pack(fill=tk.X)
        frame1_channel_column1 = tk.Frame(frame1_channel)
        frame1_channel_column1.pack(side=tk.LEFT, fill=tk.Y)
        frame1_channel_column2 = tk.Frame(frame1_channel)
        frame1_channel_column2.pack(side=tk.RIGHT, fill=tk.Y)

        self.urls_limit_label = tk.Label(
            frame1_channel_column1, text="频道接口数量:", width=12
        )
        self.urls_limit_label.pack(side=tk.LEFT, padx=4, pady=8)
        self.urls_limit_entry = tk.Entry(frame1_channel_column1)
        self.urls_limit_entry.pack(side=tk.LEFT, padx=4, pady=8)
        self.urls_limit_entry.insert(15, config.urls_limit)
        self.urls_limit_entry.bind("<KeyRelease>", self.update_urls_limit)

        self.ipv_type_label = tk.Label(
            frame1_channel_column2, text="接口协议类型:", width=12
        )
        self.ipv_type_label.pack(side=tk.LEFT, padx=4, pady=8)
        self.ipv_type_combo = ttk.Combobox(frame1_channel_column2)
        self.ipv_type_combo.pack(side=tk.LEFT, padx=4, pady=8)
        self.ipv_type_combo["values"] = ("ipv4", "ipv6", "all")
        self.ipv_type_combo.current(0)
        self.ipv_type_combo.bind("<<ComboboxSelected>>", self.update_ipv_type)

        frame1_sort = tk.Frame(frame1)
        frame1_sort.pack(fill=tk.X)

        self.open_sort_label = tk.Label(frame1_sort, text="开启测速排序:", width=12)
        self.open_sort_label.pack(side=tk.LEFT, padx=4, pady=8)
        self.open_sort_var = tk.BooleanVar(value=config.open_sort)
        self.open_sort_checkbutton = ttk.Checkbutton(
            frame1_sort,
            variable=self.open_sort_var,
            onvalue=True,
            offvalue=False,
            command=self.update_open_sort,
        )
        self.open_sort_checkbutton.pack(side=tk.LEFT, padx=4, pady=8)

        frame1_sort_params = tk.Frame(frame1)
        frame1_sort_params.pack(fill=tk.X)
        frame1_sort_params_column1 = tk.Frame(frame1_sort_params)
        frame1_sort_params_column1.pack(side=tk.LEFT, fill=tk.Y)
        frame1_sort_params_column2 = tk.Frame(frame1_sort_params)
        frame1_sort_params_column2.pack(side=tk.RIGHT, fill=tk.Y)

        self.response_time_weight_label = tk.Label(
            frame1_sort_params_column1, text="响应时间权重:", width=12
        )
        self.response_time_weight_label.pack(side=tk.LEFT, padx=4, pady=8)
        self.response_time_weight_entry = tk.Entry(frame1_sort_params_column1)
        self.response_time_weight_entry.pack(side=tk.LEFT, padx=4, pady=8)
        self.response_time_weight_entry.insert(0, config.response_time_weight)
        self.response_time_weight_entry.bind(
            "<KeyRelease>", self.update_response_time_weight
        )

        self.resolution_weight_label = tk.Label(
            frame1_sort_params_column2, text="分辨率权重:", width=12
        )
        self.resolution_weight_label.pack(side=tk.LEFT, padx=4, pady=8)
        self.resolution_weight_entry = tk.Entry(frame1_sort_params_column2)
        self.resolution_weight_entry.pack(side=tk.LEFT, padx=4, pady=8)
        self.resolution_weight_entry.insert(0, config.resolution_weight)
        self.resolution_weight_entry.bind("<KeyRelease>", self.update_resolution_weight)

        frame1_domain_blacklist = tk.Frame(frame1)
        frame1_domain_blacklist.pack(fill=tk.X)

        self.domain_blacklist_label = tk.Label(
            frame1_domain_blacklist, text="域名黑名单:", width=12
        )
        self.domain_blacklist_label.pack(side=tk.LEFT, padx=4, pady=8)
        self.domain_blacklist_text = scrolledtext.ScrolledText(
            frame1_domain_blacklist, height=5
        )
        self.domain_blacklist_text.pack(
            side=tk.LEFT, padx=4, pady=8, expand=True, fill=tk.BOTH
        )
        self.domain_blacklist_text.insert(tk.END, ",".join(config.domain_blacklist))
        self.domain_blacklist_text.bind("<KeyRelease>", self.update_domain_blacklist)

        frame1_url_keywords_blacklist = tk.Frame(frame1)
        frame1_url_keywords_blacklist.pack(fill=tk.X)

        self.url_keywords_blacklist_label = tk.Label(
            frame1_url_keywords_blacklist, text="关键字黑名单:", width=12
        )
        self.url_keywords_blacklist_label.pack(side=tk.LEFT, padx=4, pady=8)
        self.url_keywords_blacklist_text = scrolledtext.ScrolledText(
            frame1_url_keywords_blacklist, height=5
        )
        self.url_keywords_blacklist_text.pack(
            side=tk.LEFT, padx=4, pady=8, expand=True, fill=tk.BOTH
        )
        self.url_keywords_blacklist_text.insert(
            tk.END, ",".join(config.url_keywords_blacklist)
        )
        self.url_keywords_blacklist_text.bind(
            "<KeyRelease>", self.update_url_keywords_blacklist
        )

        frame2_open_online_search = tk.Frame(frame2)
        frame2_open_online_search.pack(fill=tk.X)

        self.open_online_search_label = tk.Label(
            frame2_open_online_search, text="开启在线搜索:", width=13
        )
        self.open_online_search_label.pack(side=tk.LEFT, padx=4, pady=8)
        self.open_online_search_var = tk.BooleanVar(value=config.open_online_search)
        self.open_online_search_checkbutton = ttk.Checkbutton(
            frame2_open_online_search,
            variable=self.open_online_search_var,
            onvalue=True,
            offvalue=False,
            command=self.update_open_online_search,
        )
        self.open_online_search_checkbutton.pack(side=tk.LEFT, padx=4, pady=8)

        frame2_favorite_list = tk.Frame(frame2)
        frame2_favorite_list.pack(fill=tk.X)

        self.favorite_list_label = tk.Label(
            frame2_favorite_list, text="关注频道:", width=13
        )
        self.favorite_list_label.pack(side=tk.LEFT, padx=4, pady=8)
        self.favorite_list_text = scrolledtext.ScrolledText(
            frame2_favorite_list, height=5
        )
        self.favorite_list_text.pack(
            side=tk.LEFT, padx=4, pady=8, expand=True, fill=tk.BOTH
        )
        self.favorite_list_text.insert(tk.END, ",".join(config.favorite_list))
        self.favorite_list_text.bind("<KeyRelease>", self.update_favorite_list)

        frame2_favorite_page_num = tk.Frame(frame2)
        frame2_favorite_page_num.pack(fill=tk.X)

        self.favorite_page_num_label = tk.Label(
            frame2_favorite_page_num, text="关注获取页数:", width=13
        )
        self.favorite_page_num_label.pack(side=tk.LEFT, padx=4, pady=8)
        self.favorite_page_num_entry = tk.Entry(frame2_favorite_page_num)
        self.favorite_page_num_entry.pack(side=tk.LEFT, padx=4, pady=8)
        self.favorite_page_num_entry.insert(0, config.favorite_page_num)
        self.favorite_page_num_entry.bind("<KeyRelease>", self.update_favorite_page_num)

        frame2_default_page_num = tk.Frame(frame2)
        frame2_default_page_num.pack(fill=tk.X)

        self.default_page_num_label = tk.Label(
            frame2_default_page_num, text="默认获取页数:", width=13
        )
        self.default_page_num_label.pack(side=tk.LEFT, padx=4, pady=8)
        self.default_page_num_entry = tk.Entry(frame2_default_page_num)
        self.default_page_num_entry.pack(side=tk.LEFT, padx=4, pady=8)
        self.default_page_num_entry.insert(0, config.default_page_num)
        self.default_page_num_entry.bind("<KeyRelease>", self.update_default_page_num)

        frame2_recent_days = tk.Frame(frame2)
        frame2_recent_days.pack(fill=tk.X)

        self.recent_days_label = tk.Label(
            frame2_recent_days, text="获取时间范围(天):", width=13
        )
        self.recent_days_label.pack(side=tk.LEFT, padx=4, pady=8)
        self.recent_days_entry = tk.Entry(frame2_recent_days)
        self.recent_days_entry.pack(side=tk.LEFT, padx=4, pady=8)
        self.recent_days_entry.insert(30, config.recent_days)
        self.recent_days_entry.bind("<KeyRelease>", self.update_recent_days)

        frame3_open_subscribe = tk.Frame(frame3)
        frame3_open_subscribe.pack(fill=tk.X)

        self.open_subscribe_label = tk.Label(
            frame3_open_subscribe, text="开启订阅源:", width=9
        )
        self.open_subscribe_label.pack(side=tk.LEFT, padx=4, pady=8)
        self.open_subscribe_var = tk.BooleanVar(value=config.open_subscribe)
        self.open_subscribe_checkbutton = ttk.Checkbutton(
            frame3_open_subscribe,
            variable=self.open_subscribe_var,
            onvalue=True,
            offvalue=False,
            command=self.update_open_subscribe,
        )
        self.open_subscribe_checkbutton.pack(side=tk.LEFT, padx=4, pady=8)

        frame3_subscribe_urls = tk.Frame(frame3)
        frame3_subscribe_urls.pack(fill=tk.X)

        self.subscribe_urls_label = tk.Label(
            frame3_subscribe_urls, text="订阅源:", width=9
        )
        self.subscribe_urls_label.pack(side=tk.LEFT, padx=4, pady=8)
        self.subscribe_urls_text = scrolledtext.ScrolledText(
            frame3_subscribe_urls, height=5
        )
        self.subscribe_urls_text.pack(
            side=tk.LEFT, padx=4, pady=8, expand=True, fill=tk.BOTH
        )
        self.subscribe_urls_text.insert(tk.END, ",".join(config.subscribe_urls))
        self.subscribe_urls_text.bind("<KeyRelease>", self.update_subscribe_urls)

        frame4_multicast = tk.Frame(frame4)
        frame4_multicast.pack(fill=tk.X)

        self.open_multicast_label = tk.Label(
            frame4_multicast, text="开启组播源:", width=9
        )
        self.open_multicast_label.pack(side=tk.LEFT, padx=4, pady=8)
        self.open_multicast_var = tk.BooleanVar(value=config.open_multicast)
        self.open_multicast_checkbutton = ttk.Checkbutton(
            frame4_multicast,
            variable=self.open_multicast_var,
            onvalue=True,
            offvalue=False,
            command=self.update_open_multicast,
        )
        self.open_multicast_checkbutton.pack(side=tk.LEFT, padx=4, pady=8)

        frame4_region_list = tk.Frame(frame4)
        frame4_region_list.pack(fill=tk.X)

        self.region_list_label = tk.Label(frame4_region_list, text="组播地区:", width=9)
        self.region_list_label.pack(side=tk.LEFT, padx=4, pady=8)
        self.region_list_text = scrolledtext.ScrolledText(frame4_region_list, height=5)
        self.region_list_text.pack(
            side=tk.LEFT, padx=4, pady=8, expand=True, fill=tk.BOTH
        )
        self.region_list_text.insert(tk.END, ",".join(config.region_list))
        self.region_list_text.bind("<KeyRelease>", self.update_region_list)

        root_operate = tk.Frame(self.root)
        root_operate.pack(fill=tk.X, pady=8, padx=120)
        root_operate_column1 = tk.Frame(root_operate)
        root_operate_column1.pack(side=tk.LEFT, fill=tk.Y)
        root_operate_column2 = tk.Frame(root_operate)
        root_operate_column2.pack(side=tk.RIGHT, fill=tk.Y)

        self.save_button = tk.Button(
            root_operate_column1, text="保存设置", command=self.save_config
        )
        self.save_button.pack(side=tk.LEFT, padx=4, pady=8)

        self.run_button = tk.Button(
            root_operate_column2, text="开始更新", command=self.on_run_update
        )
        self.run_button.pack(side=tk.LEFT, padx=4, pady=8)

        version_frame = tk.Frame(self.root)
        version_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.version_label = tk.Label(
            version_frame, text=self.version, fg="gray", anchor="se"
        )
        self.version_label.pack(side=tk.RIGHT, padx=5, pady=5)

        self.author_label = tk.Label(
            version_frame,
            text="by Govin",
            fg="gray",
            anchor="se",
        )
        self.author_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.project_link = tk.Label(
            version_frame, text="访问项目主页", fg="blue", cursor="hand2"
        )
        self.project_link.pack(side=tk.LEFT, padx=5, pady=5)
        self.project_link.bind(
            "<Button-1>",
            lambda e: webbrowser.open_new_tab("https://github.com/Guovin/TV"),
        )

        root_progress = tk.Frame(self.root)
        root_progress.pack(fill=tk.X)

        self.progress_bar = ttk.Progressbar(
            root_progress, length=300, mode="determinate"
        )
        self.progress_bar.pack_forget()
        self.progress_label = tk.Label(root_progress, text="进度: 0%")
        self.progress_label.pack_forget()
        self.view_result_link = tk.Label(
            root_progress, text="", fg="blue", cursor="hand2"
        )
        self.view_result_link.bind(
            "<Button-1>",
            self.view_result_link_callback,
        )
        self.view_result_link.pack_forget()


if __name__ == "__main__":
    root = tk.Tk()
    tkinter_ui = TkinterUI(root)
    tkinter_ui.init_UI()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = 500
    height = 700
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.mainloop()
